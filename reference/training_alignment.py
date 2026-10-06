"""Explicit real-interface unit/time alignment, without clipping or extrapolation.

This module does not modify native recordings or initialize a training model.
The formula matches the real project's simulated_gripper_to_dataset after
converting total two-finger opening to the adapter's single-finger input.
"""
import numpy as np

TOTAL_GRIPPER_OPEN_M = .1
REAL_GRIPPER_OPEN_RAD = -4.5
LIFT_MM_PER_M = 1000.


def real_interface_units(values, validate_opening=True):
    values = np.asarray(values, dtype=np.float64)
    if values.ndim != 2 or values.shape[1] != 18 or not np.isfinite(values).all():
        raise ValueError('Expected finite N x 18 state/action array')
    opening = values[:, [6, 13]]
    if validate_opening and ((opening < -1e-7).any() or (opening > TOTAL_GRIPPER_OPEN_M+1e-7).any()):
        raise ValueError('Total gripper opening outside factory range; do not silently clip')
    result = values.copy()
    result[:, [6, 13]] *= REAL_GRIPPER_OPEN_RAD/TOTAL_GRIPPER_OPEN_M
    result[:, 17] *= LIFT_MM_PER_M
    return result


def sim_interface_units(values):
    """Exact inverse unit conversion; command clipping is a separate operation."""
    values = np.asarray(values, dtype=np.float64)
    if values.ndim != 2 or values.shape[1] != 18 or not np.isfinite(values).all():
        raise ValueError('Expected finite N x 18 state/action array')
    result = values.copy()
    result[:, [6, 13]] *= TOTAL_GRIPPER_OPEN_M/REAL_GRIPPER_OPEN_RAD
    result[:, 17] /= LIFT_MM_PER_M
    return result


def align_episode(timestamps, state, action, source_fps=10, target_fps=30):
    """Return timestamps, measured states, absolute targets and held RGB indices.

    Last output timestamp equals the last input timestamp. Never borrow frames
    from another episode or synthesize a state beyond the recorded endpoint.
    """
    t = np.asarray(timestamps, dtype=np.float64)
    state, action = real_interface_units(state), real_interface_units(action)
    if source_fps != 10 or target_fps != 30:
        raise ValueError('This contract is specifically 10 Hz to 30 Hz')
    if t.ndim != 1 or not len(t) or len(t) != len(state) or len(t) != len(action):
        raise ValueError('Episode arrays have inconsistent lengths')
    if not np.isfinite(t).all() or not np.allclose(t, np.arange(len(t))/source_fps, atol=1e-5, rtol=0):
        raise ValueError('Nonuniform native timestamps')
    # Use the exact acquisition grid after validating its floating-point drift.
    native = np.arange(len(t), dtype=np.float64)/source_fps
    target = np.arange((len(t)-1)*3+1, dtype=np.float64)/target_fps
    rgb_indices = np.minimum(np.arange(len(target))//3, len(t)-1)
    interpolate = lambda data: np.stack([
        np.interp(target, native, data[:, i]) for i in range(18)], axis=1)
    return dict(timestamp=target, state=interpolate(state), action=interpolate(action),
                rgb_source_frame=rgb_indices)
