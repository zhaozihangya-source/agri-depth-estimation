# Depth Validation Notes

This note keeps the project honest: the current output is a relative depth cue for
agricultural scenes, not a calibrated metric-distance sensor and not a finished robot
obstacle-avoidance system.

## 1. Current Evidence

| Evidence | Status | File / note |
|---|---|---|
| Own-shot chestnut-orchard examples | Present | `assets/depth_demo_1.jpg`, `assets/depth_demo_2.jpg`, `assets/depth_demo_3.jpg` |
| Dense relative depth visualization | Present | Demo images combine RGB and predicted depth |
| MPS/local inference script | Present | `depth_estimate.py` |
| Metric distance calibration | Missing | Needs scale reference or ground truth |
| Downstream robot validation | Missing | No navigation stack or control loop |

## 2. Failure Modes to Track

| Case type | Expected failure | Why it matters | Next action |
|---|---|---|---|
| Overexposure / harsh sunlight | Depth boundaries can become unstable | Field lighting changes quickly | Add overexposed examples and compare outputs |
| Dense branch occlusion | Fine branches can confuse relative ordering | Orchard canopy is cluttered | Pair with detector boxes and manual review |
| Low-texture ground | Smooth soil/grass may have weak depth cues | Ground distance is important for robots | Add known-distance markers |
| Camera tilt / unusual pose | Relative gradient may be visually plausible but geometrically wrong | Robots need stable pose assumptions | Record camera pose or use calibration targets |
| Similar foreground/background texture | Nearby branches and distant branches can look similar | False near/far ranking affects planning | Log ranking errors by target box |

## 3. Validation Plan

| Step | Output | Resume-safe value |
|---|---|---|
| Add known-distance ruler or tree-row reference | Scale-check examples | Shows awareness of metric calibration |
| Pair depth maps with detection boxes | Near/far ranking table | Turns depth into actionable perception cue |
| Build failure-case gallery | 6-10 annotated examples | Shows honest model evaluation |
| Compare original image vs depth map | Qualitative report | Useful for interviews and project README |

## 4. Resume-Safe Wording

Current safe wording:

> Applied Depth Anything V2 to own-shot chestnut-orchard images to generate dense relative
> depth maps, using monocular depth as a low-cost perception cue for canopy distance and
> obstacle-awareness exploration.

Do not claim yet:

- Metric distance estimation in meters.
- Completed robot obstacle avoidance.
- Stereo/LiDAR-level depth accuracy.
- Real-time embedded deployment.

## 5. Next Actions

1. Add 6-10 labeled failure-case examples.
2. Add known-distance references for scale sanity checks.
3. Combine detector boxes from the chestnut CV pipeline with depth ranking.
4. Document where relative depth is reliable and where it fails.
