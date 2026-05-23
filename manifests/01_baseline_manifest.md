รายงานสถาปัตยกรรมวิศวกรรม: Reproducible Source Manifest สำหรับโครงการ CeXaR

1. หลักการทางวิศวกรรมและเกณฑ์มาตรฐานความแม่นยำ (Engineering Foundations & Criteria)

การสร้าง Baseline ที่มีคุณสมบัติการตรวจสอบซ้ำได้ (Reproducible) ในการจำแนกภาพรังสีทรวงอก (CXR) ถือเป็นปัจจัยวิกฤตทางกลยุทธ์ของโครงการ CeXaR ความท้าทายพื้นฐานในโดเมนนี้คือปัญหา Patient-level data leakage ซึ่งมักเกิดขึ้นเมื่อภาพจากคนไข้คนเดียวกันถูกแยกกระจายไปอยู่ในทั้ง Training และ Test set ส่งผลให้โมเดลจดจำคุณลักษณะทางกายวิภาค (Anatomical characteristics) หรือ Artifact จากเครื่องสแกนเฉพาะรายบุคคล แทนที่จะวินิจฉัยรอยโรคจริง สถาปัตยกรรมนี้จึงบังคับใช้โปรโตคอลการแบ่ง Split ตาม Patient ID (70/10/20) เพื่อให้มั่นใจใน Generalization ต่อคนไข้ใหม่

นอกจากนี้ ปัญหา Class Imbalance ที่รุนแรงในชุดข้อมูล CXR (เช่น กรณีโรค Hernia ที่มีตัวอย่างน้อยมาก) ทำให้ Binary Cross-Entropy (BCE) แบบมาตรฐานมีประสิทธิภาพต่ำ รายงานฉับนี้จึงกำหนดให้ใช้ Focal Loss เป็นมาตรฐานหลัก โดยมีสูตรคำนวณคือ: FL(p_t) = -\alpha_t (1 - p_t)^\gamma \log(p_t) โดยกำหนดค่าพารามิเตอร์ตามเกณฑ์มาตรฐานที่ \gamma = 2 และ \alpha = 1 เพื่อเพิ่มน้ำหนักให้กับตัวอย่างที่โมเดลจำแนกได้ยาก

ในเชิงสถาปัตยกรรม การเลือกใช้ Global Pooling มีผลอย่างมากต่อความแม่นยำและการทำ Saliency Maps รายงานนี้ระบุว่า PCAM (Probabilistic Class Activation Map) และ LSE (Log-Sum-Exponential) pooling มีประสิทธิภาพเหนือกว่า Global Average Pooling (GAP) ทั่วไปในการทำ Weakly supervised pathology localization ซึ่งจำเป็นสำหรับการตรวจสอบโดยรังสีแพทย์ในขั้นตอน Grad-CAM ต่อไป

เกณฑ์การให้คะแนน Reproducibility Score (1-5):

* 5 (Excellent): มี Code, Weights ครบถ้วน และรันได้ทันทีด้วย API มาตรฐาน
* 4 (Good): ข้อมูลเกือบครบ แต่อาจต้องปรับปรุง Code หรือจัดการ Checkpoint แมนนวล
* 3 (Fair): ข้อมูลเชิงทฤษฎีดีแต่ขาดองค์ประกอบสำคัญในการรัน เช่น ขาด Checkpoint หรือ Split ไม่ชัดเจน
* 2 (Limited): ข้อมูลไม่เพียงพอสำหรับการสร้าง Baseline
* 1 (Poor): ไม่แนะนำให้ใช้เนื่องจากข้อผิดพลาดเชิงโครงสร้างหรือประสิทธิภาพต่ำเกินเกณฑ์

เมื่อวางรากฐานทางทฤษฎีและเกณฑ์การคัดเลือกแล้ว ส่วนถัดไปจะระบุกลุ่ม Candidate ระดับ Tier 1 ที่มีศักยภาพสูงสุดในการรัน Baseline ทันที

2. Tier 1: Must Test - แหล่งข้อมูลมาตรฐานสำหรับการทดสอบทันที (Reproducibility Score 4-5)

Candidate Name	Year	Paper URL	Code URL	Pretrained Weights URL	Dataset	Model/Backbone	Split Protocol	Preprocessing	Eval Script	Reported Metrics (AUROC)	Repro Score	Codex/Claude Next Step
TorchXRayVision (XRV)	2022	https://proceedings.mlr.press/v172/cohen22a/cohen22a.pdf	https://github.com/mlmed/torchxrayvision	https://huggingface.co/torchxrayvision/resnet50-res512-all	NIH, CheXpert, MIMIC-CXR	DenseNet121, ResNet50	Multi-dataset (20% test)	Resizing, Intensity Norm [-1024, 1024] (Critical)	xrv.models.get_model	NIH ResNet50: Cardiomegaly (0.90), Effusion (0.86)	5	Highlight: ต้องใช้ค่า Normalization ช่วง [-1024, 1024] เท่านั้น ห้ามใช้ ImageNet Norm
arnoweng CheXNet	2017	https://arxiv.org/abs/1711.05225	https://github.com/arnoweng/CheXNet	https://github.com/arnoweng/CheXNet/raw/master/model.pth.tar	NIH ChestX-ray14	DenseNet121	Patient-level (70/10/20)	Resize 256, Ten-Crop 224, ImageNet Norm	python model.py	NIH: Atelectasis (0.8294), Effusion (0.8870)	4.5	ตรวจสอบ read_data.py เพื่อดู Logic การทำ Ten-Crop ช่วง Inference
rajpurkarlab CheXzero	2022	https://nature.com/articles/s41551-022-00936-9	https://github.com/rajpurkarlab/CheXzero	https://drive.google.com/drive/folders/1makFLiEMbSleYltaRxw81aBhEDMpVwno	MIMIC-CXR, CheXpert	CLIP (ViT-B/32)	Zero-Shot (Public Test Set)	Resize 224, HDF5 storage format	python eval.py	CheXpert Zero-shot: Effusion (0.9317), Edema (0.8994)	4.25	ตรวจสอบ eval.py เพื่อดูการคำนวณ Cosine Similarity ระหว่าง Image และ Text Prompt
dstrick17 DacNet	2025	https://arxiv.org/abs/2505.06646	https://github.com/dstrick17/DacNet	https://huggingface.co/spaces/cfgpp/DACNet	NIH ChestX-ray14	DenseNet121, ViT-Base	Patient-level (70/10/20)	RandomResizedCrop, Focal Loss, AdamW	python scripts/Dacnet.py	NIH Test: Mean AUC (0.85), Avg F1 (0.39)	4	Must Verify: ตรวจสอบการเพิ่ม F1-score จาก 0.08 เป็น 0.39 เมื่อใช้ Focal Loss เทียบกับ BCE
jfhealthcare CheXpert	2020	https://stanfordmlgroup.github.io/competitions/chexpert/	https://github.com/jfhealthcare/Chexpert	https://github.com/jfhealthcare/Chexpert/blob/master/config/pre_train.pth	CheXpert	DenseNet (PCAM/LSE Pooling)	200 patients (Val split)	U-Ones/U-Zeros mapping	python test.py	CheXpert: Edema (0.9436), Effusion (0.9166)	3.75	ศึกษาโครงสร้าง Custom Pooling Heads เพื่อเพิ่มความแม่นยำใน Localization

หลังจากพิจารณา Baseline หลักที่พร้อมใช้งานแล้ว ส่วนต่อไปจะกล่าวถึงแหล่งข้อมูลอ้างอิงที่มีคุณค่าเชิงเทคนิคแต่อาจขาดองค์ประกอบบางประการในการรันแบบ End-to-end

3. Tier 2: Useful Reference - แหล่งข้อมูลอ้างอิงเชิงสถาปัตยกรรม

โมเดลในกลุ่มนี้มีประโยชน์ในการศึกษาเทคนิคขั้นสูง เช่น Self-supervised pre-training หรือการประมวลผลความละเอียดสูง (1024x1024) เพื่อลดการพึ่งพา Label และเพิ่มความคมชัดของผลลัพธ์

Candidate	Paper URL	Code URL	Missing piece	Why still useful	Repro Score
MedicalPatchNet	Insufficient evidence	https://github.com/TruhnLab/MedicalPatchNet	Checkpoints	รองรับ High-resolution (1024x1024) และการประเมินด้วย CheXlocalize	3
MoCo-CXR	https://openreview.net/forum?id=LO7Su0-dPJl	https://github.com/stanfordmlgroup/MoCo-CXR	Full weights set	สาธิตความได้เปรียบของ Contrastive pre-training เหนือ ImageNet initialization	3
MedCLIP	https://arxiv.org/abs/2210.10163	https://github.com/RyanWangZf/MedCLIP	Checkpoints for classification	ใช้ Decoupled semantic matching เพื่อลดปัญหา False-negative alignment	3
hi-ml	https://arxiv.org/abs/2204.09817	https://github.com/microsoft/hi-ml	Task-specific weights	มีโมเดล BioViL สำหรับการทำ Phrase grounding และ Hybrid architectures	3
DuEL-Med	Exact URL not found in current sources	https://github.com/jink-ucla/DuEL-Med	Full dataset pre-processing	เน้นการทำงาน Multi-task ระหว่าง Classification และ Report generation	2.5
SurgicalAggregation	https://arxiv.org/abs/2301.06683	https://github.com/BioIntelligence-Lab/SurgicalAggregation	Standalone execution weights	นำเสนอเทคนิค Federated learning (FedBN+) สำหรับ Multi-site datasets	2.5

นอกจากแหล่งอ้างอิงเชิงเทคนิคแล้ว ยังมีงานวิจัยบางส่วนที่ควรรับทราบไว้ในฐานะข้อมูลพื้นฐานแต่ไม่ควรนำมาใช้เป็น Baseline

4. Tier 3: Background Only - แหล่งข้อมูลสนับสนุนทางทฤษฎี

Candidate	URL	Reason not baseline
ONNX-CXR	https://github.com/jayshah1819/CUDA-Accelerated-Chest-X-Ray-Classification-with-ONNX	เน้นเฉพาะ Hardware acceleration และ ONNX Runtime เท่านั้น
Stomper10 CheXpert	https://github.com/Stomper10/CheXpert	ประสิทธิภาพ (mAUC ~0.85) ต่ำกว่าเกณฑ์มาตรฐานของ Stanford อย่างชัดเจน
dawoodrehman44 SD-LoRA-CXR	https://github.com/dawoodrehman44/Stable-Diffusion-with-LoRA	เน้นการสร้าง Synthetic data เพื่อแก้ปัญหา Fairness ไม่ใช่ตัวโมเดลวินิจฉัยหลัก
etetteh OoD_Gen	https://github.com/etetteh/OoD_Gen-Chest_Xray	เน้นการศึกษา Out-of-distribution และไม่มี Checkpoint SOTA ที่พร้อมใช้

5. การตรวจสอบหลักฐานที่ขาดหายและประเด็นความเสี่ยง (Missing Evidence & Audit)

Claim	Missing evidence	Why it matters	What to verify next
arnoweng Checkpoint Compatibility	รุ่นของ PyTorch ที่รองรับ	รุ่น 0.4.0 มีปัญหา state_dict key mismatch กับ PyTorch รุ่นใหม่	ตรวจสอบการทำ Key Mapping (เช่น module. prefix) ระหว่างโหลด Weights
jfhealthcare Evaluation	Local validation results	ผลลัพธ์ส่วนใหญ่มาจาก Hidden test set ซึ่งตรวจสอบเองไม่ได้	บังคับทดสอบบน 200-patient "valid_list.txt" เพื่อยืนยันความแม่นยำเบื้องต้น
Shortcut Learning Risk	เครดิตความแม่นยำที่แท้จริง	โมเดลอาจจดจำ "Token, Hospital labels หรือ Pacemakers" แทนที่จะเป็นรอยโรค	ใช้ Grad-CAM ตรวจสอบว่าโมเดลไม่ได้ Focus ที่วัตถุแปลกปลอมหรือขอบภาพ
Uncertainty Policy	ผลกระทบของ U-Ones/U-Zeros	การใช้ U-Ones อาจทำให้ Sensitivity สูงเกินจริง (Artificially inflated)	ตรวจสอบ Label mapping ในสคริปต์ Preprocessing ว่าสอดคล้องกับมาตรฐาน CeXaR หรือไม่

เพื่อให้การเปลี่ยนผ่านจากข้อมูลสู่การลงมือทำมีประสิทธิภาพ ส่วนสุดท้ายจะระบุขั้นตอนปฏิบัติสำหรับ Codex หรือ Claude Code

6. แผนการตรวจสอบและรันระบบ (Codex/Claude Clone-and-Inspect Plan)

1. ลำดับการ Clone Repository (ตามความสำคัญ):
  * https://github.com/mlmed/torchxrayvision (Priority 1: Unified API และ Weights ที่หลากหลายที่สุด)
  * https://github.com/arnoweng/CheXNet (Priority 2: มาตรฐานอ้างอิง NIH)
  * https://github.com/dstrick17/DacNet (Priority 3: Focal Loss Implementation)
  * https://github.com/rajpurkarlab/CheXzero (Priority 4: Zero-shot/Contrastive Learning)
2. ข้อมูลดิบสำหรับการฝึก (Data Acquisition):
  * NIH ChestX-ray14: https://www.kaggle.com/datasets/nih-chest-xrays/data
3. ไฟล์วิกฤตที่ต้อง Inspect:
  * arnoweng: ตรวจสอบ read_data.py เพื่อยืนยันการทำ Ten-Crop และ model.py สำหรับ nn.Sigmoid() ชั้นสุดท้าย
  * TorchXRayVision: ตรวจสอบ torchxrayvision/datasets.py เพื่อดู Logic การทำ Intensity Normalization ([-1024, 1024])
  * CheXzero: ตรวจสอบ eval.py เพื่อระบุตำแหน่งไฟล์ data/cxr.h5 และการจัดการ Text prompt
  * DacNet: ตรวจสอบ scripts/Dacnet.py เพื่อดูการตั้งค่า AdamW และ Focal Loss (\gamma=2, \alpha=1)
4. จุดเสี่ยง (Risks) ที่ต้องตรวจสอบโดยละเอียด:
  * Normalization Conflict: TorchXRayVision ใช้ช่วง [-1024, 1024] ในขณะที่รายอื่นมักใช้ ImageNet Norm (0-1 range) หากใช้ผิดโมเดลจะให้ผลลัพธ์ที่ผิดพลาดโดยสิ้นเชิง
  * Label Mapping: ตรวจสอบนโยบาย Uncertainty (U-Ones vs U-Zeros) ในสคริปต์โหลดข้อมูล เพื่อป้องกันการเกิด Bias ในผลลัพธ์
  * Patient Leakage: ตรวจสอบว่า labels/test_list.txt หรือไฟล์ Split อื่นๆ ไม่มีการปนเปื้อนของภาพจากคนไข้คนเดียวกันระหว่างชุด Train และ Test
5. สรุป 3 อันดับ Baseline Candidates ที่ควรเริ่มทดสอบก่อน:
  1. TorchXRayVision: เนื่องจากมีความพร้อมสูงสุดและรองรับหลาย Datasets
  2. arnoweng CheXNet: เพื่อกำหนดค่ามาตรฐาน (Golden Baseline) บน NIH Dataset
  3. DacNet: เพื่อประเมินประสิทธิภาพของการแก้ปัญหา Class Imbalance ด้วย Focal Loss เทียบกับ BCE ปกติ
