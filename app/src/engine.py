from tqdm import tqdm
import torch


def train_fn(model, data_loader, optimizer):
    """calc loss and optim step over dataloader

    Args:
        model (torch.nn.Module): trainable model
        data_loader (torch.utils.data.Dataloader): dataloader
        optimizer (torch.optim): optimizer of loss func

    Returns:
        float: total loss on dataloader
    """
    model.train()
    total_loss = 0
    tk = tqdm(data_loader, total=len(data_loader))
    for data in tk:
        optimizer.zero_grad()
        preds = model(data['images'])
        loss = model.compute_loss(preds, data['labels'])
        loss.backward()
        optimizer.step()

        tk.set_description('loss: ' + str(loss.item()))

        total_loss += loss.item()

    return total_loss / len(data_loader)


def eval_fn(model, data_loader):
    """evaluate model with dataloader

    Args:
        model (torch.nn.Module): model
        data_loader (torch.utils.data.Dataloader): dataloader

    Returns:
        [
            torch.tensor: gt_labels in dataloader,
            torch.tensor: prediction matricies with probabilities over
            timesteps in dataloader,
            float: total loss on dataloader
        ]
    """
    model.eval()
    total_loss = 0
    total_preds = []
    total_gt = []

    tk = tqdm(data_loader, total=len(data_loader))
    for data in tk:
        with torch.no_grad():
            preds = model(data['images'])
            loss = model.compute_loss(preds, data['labels'])
            total_loss += loss.item()

            total_preds.append(preds)
            total_gt.append(data['labels'])

    return total_gt, total_preds, total_loss / len(data_loader)
