import torch
import numpy as np
from typing import Dict, List
from pyctcdecode import BeamSearchDecoderCTC


def _decode_sample(sample, blank_id, num_to_char):
    label = ''
    for i in sample:
        if i == blank_id:
            break
        label += num_to_char.get(i, '')
    return label

def decode_gts(batch: torch.Tensor, blank_id: int, num_to_char: Dict) -> List:
    """decode ground truth labels

    Args:
        labels (torch.Tensor):
        blank_id (int): 
        num_to_char (Dict):

    Returns:
        List: gt texts
    """
    if isinstance(batch[0], torch.Tensor):
        batch = batch.detach().cpu().numpy()
    results = []
    for label in batch:
        decoded = _decode_sample(label, blank_id, num_to_char)
        results.append(decoded)
    return results


def ctc_decode(raw_preds) -> List:
    """ decode raw output bathces from NN

    Args:
        raw_preds (list[torch.tensor]): list of predictions in shape [T, B, M]
        T - timestemps
        B - batch size
        M - max label length

    Returns:
        List: list of bathes
    """
    preds, blank = ctc_proba_calc(raw_preds)
    reduced = reduce_ctc_decoded_preds(preds, blank)
    return reduced


def ctc_proba_calc(raw_preds):
    """apply softmax and argmax to proba matrix

    Args:
        raw_preds (list[torch.tensor]): list of predictions in shape [T, B, M]
        T - timestemps
        B - batch size
        M - max label length

    Returns:
        list: list of batches
        int: blank index
    """
    blank = raw_preds[0].shape[-1] - 1
    preds = []
    for batch in raw_preds:
        batch = batch.permute(1, 0, 2)
        batch = torch.softmax(batch, 2)
        batch = torch.argmax(batch, 2)
        batch = batch.detach().cpu().numpy()
        preds.append(batch)
    return preds, blank


def reduce_ctc_decoded_preds(preds, blank):
    """reduce duplicates ctc

    Args:
        preds (torch.Tensor): ctc decoded preds

    Returns:
        List reduced labels
    """
    pad_to = preds[0].shape[-1]
    reduced_preds = []
    for batch in preds:
        batch_preds = []
        for sample in batch:
            sample = [sample[0]] + \
                [c for i, c in enumerate(sample[1:]) if c != sample[i]]
            sample = list(filter(lambda i: i != blank, sample))
            sample = np.pad(sample, (0, pad_to-len(sample),),
                            constant_values=blank, mode='constant')
            batch_preds.append(sample)
        reduced_preds.append(batch_preds)
    return reduced_preds


# GREEDY SEARCH

def greedy_decode(batch, blank_id: int, num_to_char: Dict):
    """ greedy search decode raw output batch from NN
    Args:
        batch (torch.tensor): prediction in shape [T, B, V]
        T - timestemps
        B - batch size
        V - vocab size

    Returns:
        List: labels
    """
    batch = batch.permute(1, 0, 2)
    batch = torch.softmax(batch, 2)
    batch = torch.argmax(batch, 2)
    batch = batch.detach().cpu().numpy()

    labels = []
    for sample in batch:
        sample = [sample[0]] + \
                [c for i, c in enumerate(sample[1:]) if c != sample[i]]
        sample = [s for s in sample if s != blank_id]
        label = _decode_sample(sample, blank_id, num_to_char)
        labels.append(label)
    return labels


# HOTWORD BEAM DECODE
def hotword_beam_search_decode(
        batch: torch.Tensor,
        decoder: BeamSearchDecoderCTC,
        top_n: int = 3, beam_width: int = 50,
        hotwords: List[str] = None
        ) -> List[List[str]]:
    """ beam search decode raw output batch from NN
    Args:
        batch (torch.tensor): prediction in shape [T, B, V]
            T - timestemps
            B - batch size
            V - vocab size
        decoder(BeamSearchDecoderCTC):
        top_n (int): top n beam search results
        hotwords(List[str]): hotwords to be more relevant in decoding

    Returns:
        List: top_n labels
    """
    result_labels = []

    batch = torch.softmax(batch, 2)
    batch_list = [b.detach().cpu().numpy() for b in batch.moveaxis(0, 1)]

    for sample in batch_list:
        labels = []
        beam_result = decoder.decode_beams(sample,
                                           beam_width=beam_width,
                                           hotwords=hotwords)
        for i in range(min(top_n, len(beam_result))):
            labels.append(beam_result[i][0])
        result_labels.append(labels)

    return result_labels
