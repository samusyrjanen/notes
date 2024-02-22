import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage.feature import local_binary_pattern

def create_lbp_dict(image_dict:dict, radius:int, n_points:int):
    lbp_dict = {}
    for img_name, img_data in image_dict.items():
        image = cv2.cvtColor(img_data.image, cv2.COLOR_BGR2GRAY)
        lbp = local_binary_pattern(image, n_points, radius, method='uniform')
        lbp_dict[img_name] = lbp
    return lbp_dict

def combine_masks(masks:list, image_dict:dict, image_name:str):
    combined_mask = image_dict[image_name].masks[masks[0]].astype(bool)
    if len(masks) > 1:
        for mask in masks[1:]:
            combined_mask = combined_mask | image_dict[image_name].masks[mask].astype(bool)
    return combined_mask

def combine_masks_as_int(masks:list, image_dict:dict, image_name:str):
    combined_mask = image_dict[image_name].masks[masks[0]].astype(np.uint8)
    if len(masks) > 1:
        for mask in masks[1:]:
            combined_mask = combined_mask | image_dict[image_name].masks[mask].astype(np.uint8)
    return combined_mask

def visualize_lbp(lbp:np.ndarray, image_dict:dict, image_name:str, masks:list):
    mask = combine_masks(masks, image_dict, image_name)
    mask_as_int = combine_masks_as_int(masks, image_dict, image_name)
    masked = cv2.bitwise_and(lbp, lbp, mask=mask_as_int)

    fig, (ax_img, ax_hist) = plt.subplots(nrows=2, ncols=1, figsize=(5, 5))
    plt.gray()
    ax_img.imshow(masked)
    ax_img.axis('off')
    n_bins = int(lbp.max() + 1)
    ax_hist.hist(lbp[mask], density=True, bins=n_bins, range=(0, n_bins))
    ax_hist.set_ylabel('Percentage')

def kullback_leibler_divergence(p, q):
    p = np.asarray(p)
    q = np.asarray(q)
    filt = np.logical_and(p != 0, q != 0)
    return np.sum(p[filt] * np.log2(p[filt] / q[filt]))

def calculate_kullback_leibler_divergence_scores(image_dict:dict, lbp_dict:dict, image_name:str, masks:list):
    score_dict = {}

    lbp = lbp_dict[image_name]
    mask = combine_masks(masks, image_dict, image_name)
    n_bins = int(lbp.max() + 1)
    hist, _ = np.histogram(lbp[mask], density=True, bins=n_bins, range=(0, n_bins))

    for name, ref in lbp_dict.items():
        mask = combine_masks(masks, image_dict, name)
        ref_hist, _ = np.histogram(ref[mask], density=True, bins=n_bins, range=(0, n_bins))
        score = kullback_leibler_divergence(hist, ref_hist)
        score_dict[name] = score
    return score_dict

def visualize_scores(score_dict:dict, image_dict:dict, image_name:str):
    top_8_matches = sorted(score_dict.items(), key=lambda x: x[1])[:8]
    worst_8_matches = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)[:8]

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5,5))
    fig.suptitle('Original image')
    ax.imshow(image_dict[image_name].image)
    ax.axis('off')
    plt.show()

    fig, ax = plt.subplots(nrows=1, ncols=8, figsize=(20,5))
    fig.suptitle('Top 8 most similar images by Kullback-Leibler divergence score (lower is more similar)')
    for i, (name, score) in enumerate(top_8_matches):
        ax[i].imshow(image_dict[name].image)
        ax[i].axis('off')
        ax[i].set_title(f'{name}\nscore {round(score, 4)}')
    plt.show()

    fig, ax = plt.subplots(nrows=1, ncols=8, figsize=(20,5))
    fig.suptitle('Top 8 least similar images by Kullback-Leibler divergence score (lower is more similar)')
    for i, (name, score) in enumerate(worst_8_matches):
        ax[i].imshow(image_dict[name].image)
        ax[i].axis('off')
        ax[i].set_title(f'{name}\nscore {round(score, 4)}')
    plt.show()
