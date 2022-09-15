import numpy as np
from math import atan2
from sklearn.cluster import DBSCAN
from typing import List, Tuple


def sort_boxes(boxes: List[np.ndarray]) -> List[np.ndarray]:
    """Sorts boxes according to the intended order of reading the text.

    Args:
        boxes (List[np.ndarray]): list of boxes consisting of
            vertices coordinates.

    Returns:
        List[np.ndarray]: list of sorted boxes.
    """
    if len(boxes) == 0:
        return [[], []]
    incline = compute_incline(boxes)
    boxes = transform_boxes(boxes, -incline)
    h_clusters = sort_boxes_by_axis(boxes, axis=1)
    sorted_boxes = []
    for cluster in h_clusters:
        v_clusters = sort_boxes_by_axis(cluster, axis=0)
        sorted_boxes.extend(np.int32(transform_boxes(v_clusters, incline)))

    return sorted_boxes


def sort_boxes_by_axis(boxes: List[np.ndarray], axis: int) -> List[List[np.ndarray]]:
    """Sorts boxes along axis by clustering.

    Args:
        boxes (List[np.ndarray]): list of boxes to sort by given axis.
        axis (int): axis by which boxes are sorted:
            sorts by abscissa if axis = 0 and
            by ordinate if axis = 1.

    Returns:
        List[List[np.ndarray]]: clusters obtained as a result of sorting:
            vertical clusters if axis = 0 and
            horizontal clusters if axis = 1.
    """
    projections = [get_box_projection(box, axis) for box in boxes]
    sep_coords = get_optimal_separation(projections, axis)
    clusters = [[] for _ in range(len(sep_coords))]
    
    for box in boxes:
        centre = sum(get_box_projection(box, axis)) // 2
        min_distance_to_sep = 10**5
        proper_cluster_idx = 0
        
        for idx, sep_coord in enumerate(sep_coords):
            distance_to_sep = centre - sep_coord
            if 0 < distance_to_sep < min_distance_to_sep:
                min_distance_to_sep = distance_to_sep
                proper_cluster_idx = idx
                
        clusters[proper_cluster_idx].append(box)
        
    if axis == 0:
        res = []
        for cluster in clusters:
            _clusters = sort_boxes_by_axis(cluster, axis=1)
            for _cluster in _clusters:
                _cluster.sort(key=lambda x: x[0][0])
                res.extend(_cluster)
        return res
    
    return clusters


def get_optimal_separation(segments: List, axis: int) -> List:
    """Finds optimal partition of segments by clustering with DBSCAN."""
    projections = np.array([[sum(segment) // 2] * 2 for segment in segments])
    lengths = np.array([segment[1] - segment[0] for segment in segments])

    if axis == 1:
        eps = (lengths.max() + 3 * lengths.mean()) / 8
    else:
        eps = lengths.mean() / 2
    if eps == 0:
        eps = 50
    clustering = DBSCAN(eps=eps, min_samples=1).fit(projections)
    
    labels = clustering.labels_
    centroids = [projections[labels == label].mean() for label in np.unique(labels)]
    centroids.sort()
    
    seps = [(centroids[i] + centroids[i-1]) // 2 for i in range(1, len(centroids))]
    
    return [0] + seps


def compute_incline(boxes: List[np.ndarray]) -> float:
    """
    Computes general incline of boxes in radians by calculating
    weighted average of all boxes inclines depending on boxes long sides.

    """
    inclines, projections = [], []
    
    for box in boxes:
        top_left, top_right = box[0], box[1]
        incline = atan2(top_right[1] - top_left[1],
                        top_right[0] - top_left[0])
        long_side_projection = top_right[0] - top_left[0]
        inclines.append(incline)
        projections.append(long_side_projection)
    
    weighted_sum = sum([angle * side for angle, side in zip(inclines, projections)])
    weighted_avg_incline = weighted_sum / sum(projections)
    
    return weighted_avg_incline


def create_rotation_matrix(angle: float) -> np.ndarray:
    """Creates rotation matrix by the angle in radians."""
    return np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle), np.cos(angle)]
    ])


def transform_dot(dot: np.ndarray, angle: float, bias: float) -> np.ndarray:
    """Transforms dot by rotating relative to the biased point."""
    rot_matrix = create_rotation_matrix(angle)
    return np.matmul(rot_matrix, dot + bias) - bias


def transform_box(box: np.ndarray, angle: float, bias: float) -> np.ndarray:
    """Transforms box vertices by rotating relative to the biased point."""
    return np.apply_along_axis(transform_dot, 1, box, angle, bias)


def transform_boxes(boxes: List[np.ndarray], angle: float) -> List[np.ndarray]:
    """Transforms boxes by rotating relative to the origin of coordinates."""
    return [transform_box(box, angle, 0) for box in boxes]


def get_box_projection(box: np.ndarray, axis: int) -> Tuple[float, float]:
    """Computes box projection on the given axis."""
    coords = [vert[axis] for vert in box]
    return min(coords), max(coords)
