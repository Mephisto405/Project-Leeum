import numpy as np
import json
from pprint import pprint

# borrowed from https://github.com/yenchenlin/nerf-pytorch/


def normalize(x):
    return x / np.linalg.norm(x)


def viewmatrix(z, up, pos):
    vec2 = normalize(z)
    vec1_avg = up
    vec0 = normalize(np.cross(vec1_avg, vec2))
    vec1 = normalize(np.cross(vec2, vec0))
    m = np.stack([vec0, vec1, vec2, pos], 1)
    return m


def render_path_spiral(c2w, up, rads, focal, zrate=.5, rots=2, N=120):
    """_summary_

    Args:
        c2w (_type_): the camera-to-world transformation
        up (_type_): the up vector
        rads (_type_): the radii of the spiral path (3x1)
        focal (_type_): _description_
        zrate (_type_): _description_
        rots (int, optional): _description_. Defaults to 2.
        N (int, optional): _description_. Defaults to 120.

    Returns:
        list: the list of 4x4 affine matrix
    """
    render_poses = []
    rads = np.array(list(rads) + [1.])

    for theta in np.linspace(0., 2. * np.pi * rots, N + 1)[:-1]:
        c = np.dot(
            c2w[:3, :4],
            np.array(
                [np.cos(theta), -np.sin(theta), -np.sin(theta * zrate), 1.]) *
            rads)
        z = normalize(c - np.dot(c2w[:3, :4], np.array([0, 0, -focal, 1.])))
        render_poses.append(
            np.concatenate([viewmatrix(z, up, c), [[0, 0, 0, 1]]], 0).tolist())
    return render_poses


def load_llff_path(base_c2w):
    """_summary_

    Args:
        base_c2w (np.ndarray): the 4x4 matrix of the centre camera
    """
    up = normalize(base_c2w[:3, 1])  # base_c2w * [0, 0, 1, 0]^T = up vector
    close_depth, inf_depth = 2, 100
    dt = .75
    focal = 1. / (((1. - dt) / close_depth + dt / inf_depth))

    # Get radii for spiral path
    tt = base_c2w[:3, 3]  # translation
    # rads = np.percentile(np.abs(tt), 90, axis=0)
    rads = (np.array(tt) * 0.5).tolist()

    render_poses = render_path_spiral(base_c2w, up, rads, focal)
    return render_poses


def get_render_poses(path, idx=0):
    with open(path) as f:
        test_transforms = json.load(f)
    transform_matrix = test_transforms["frames"][idx]["transform_matrix"]
    transform_matrix = np.array(transform_matrix)
    render_poses = load_llff_path(transform_matrix)
    return render_poses


if __name__ == "__main__":
    np.set_printoptions(precision=2)

    test_transforms_path = "/workspace/iycho/LeeumVid2Obj/data/dragonjar_half/transforms.json"
    render_poses = get_render_poses(test_transforms_path)
    print(np.array(render_poses).shape)
    pprint(np.array(render_poses))

    # for debugging
    # import matplotlib.pyplot as plt
    # import seaborn as sns

    # render_poses = np.array(render_poses)
    # px = render_poses[:, :, 3]
    # sns.set(style="darkgrid")

    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')

    # x = px[:, 0]
    # y = px[:, 1]
    # z = px[:, 2]

    # ax.set_xlabel("x")
    # ax.set_ylabel("y")
    # ax.set_zlabel("z")

    # ax.scatter(x, y, z)

    # plt.show()