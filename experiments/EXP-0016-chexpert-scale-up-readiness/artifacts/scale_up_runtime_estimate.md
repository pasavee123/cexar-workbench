# EXP-0016: Scale-Up Runtime and Storage Estimate

## Reference (EXP-0013 Observed)

| Metric | Value |
|--------|-------|
| Images processed | 100 |
| Hardware | CPU i7-12700H |
| RAD-DINO embedding shape | [100, 768] |
| Runtime | 90.35 seconds |
| Per-image rate | ~0.90 seconds/image |

## Estimated Scaling

| Sample Size | Embedding Shape | File Size (MB) | Est. CPU Runtime | GPU Recommended? |
|-------------|----------------|----------------|------------------|------------------|
| 1,000 images | [1000, 768] | 2.93 MB | 15.06 min | No (optional) |
| 5,000 images | [5000, 768] | 14.65 MB | 1.2549 hours | Yes |
| 10,000 images | [10000, 768] | 29.3 MB | 2.5097 hours | Yes |

## Disk Storage for Embeddings

| Format | Per 1k images | Per 5k images | Per 10k images |
|--------|--------------|--------------|---------------|
| float32 .npy | ~2.93 MB | ~14.65 MB | ~29.3 MB |

## Recommendations

- 1,000 images: feasible on CPU (<1 hour).
- 5,000 images: GPU strongly recommended (several hours on CPU).
- 10,000 images: requires GPU for practical throughput.
- Full dataset (223648 images): requires GPU batch processing.

## Risks

- CPU-only inference for >1,000 images becomes impractical (wall-clock time exceeds practical iteration loop).
- Disk space is minimal (float32 embeddings are compact).
- RAM: embedding matrix for 10,000 images is ~30 MB; negligible.
- For full-scale (223,000+ images), batch processing with GPU is required; estimated 50+ hours on single-core CPU.

## Notes

- This estimate is for RAD-DINO embedding generation only, not training.
- Linear-probe training adds minimal overhead (seconds to minutes on CPU for these sizes).
- Actual RAD-DINO throughput may vary with image resolution, preprocessing, and batch size.
