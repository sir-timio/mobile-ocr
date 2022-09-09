import torch
import numpy as np
from typing import List


def ctc_decode_predictions(raw_preds) -> List:
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
        int: timesteps
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
            sample = np.pad(sample, (0, pad_to-len(sample)),
                            constant_values=blank)
            batch_preds.append(sample)
        reduced_preds.append(batch_preds)
    return reduced_preds


def decode(batch, decoder, blank='#'):
    """decode vector of nums into string with num to char map

    Args:
        batch (torch.tensor): batch of vectorized labels
        decoder (dict): map from number to character
        blank (str, optional): blank symbol to delete it. Defaults to '#'.

    Returns:
        list: batch of decoded strings
    """
    decoded = []
    for s in batch:
        label = ''.join([decoder[w.item()]
                         for w in s]).replace(blank, '')
        decoded.append(label)
    return decoded