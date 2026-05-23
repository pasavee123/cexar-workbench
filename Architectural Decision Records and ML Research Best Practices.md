รายงานมาตรฐานทางวิศวกรรมสำหรับการทดลอง ML และ Software (Engineering Standard Pack)

ในฐานะสถาปนิกอาวุโส MLOps และผู้เชี่ยวชาญด้านโครงสร้างพื้นฐาน AI มาตรฐาน "Engineering Standard Pack" นี้ถูกออกแบบมาเพื่อสร้างรากฐานที่แข็งแกร่งสำหรับการวิจัยและพัฒนา AI ยุคใหม่ โดยมุ่งเน้นไปที่การสร้าง Socio-technical contract (สัญญาทางสังคมและเทคนิค) ระหว่างนักวิจัย วิศวกร และ AI Agent เพื่อให้มั่นใจว่าทุกการตัดสินใจและการทดลองมีความโปร่งใส ตรวจสอบได้ และทำซ้ำได้จริง


--------------------------------------------------------------------------------


1. บทนำและความสำคัญเชิงกลยุทธ์ (Introduction & Strategic Importance)

การสร้างมาตรฐานทางวิศวกรรมไม่ใช่เพียงการกำหนดโฟลเดอร์ แต่คือการวางรากฐานของ Reliable Data Science ตามแนวทางของ Cookiecutter Data Science (CCDS) V2 และหลักการ "10 Rules of Reliable Data Science" เราต้องตระหนักถึงความแตกต่างเชิงสถาปัตยกรรมดังนี้:

* Deterministic Software: ระบบซอฟต์แวร์แบบดั้งเดิมที่มี Logic ตายตัวและคาดเดาผลลัพธ์ได้จาก Code
* Experiment-focused ML Systems: ระบบที่พฤติกรรมอุบัติขึ้น (Emergent behavior) จากข้อมูล การตั้งค่า และพลวัตของการเทรน ตามแนวทางของ Software Sustainability Institute (SSI) ความน่าเชื่อถือไม่ได้อยู่ที่ Code อย่างเดียว แต่อยู่ที่ "กระบวนการ" (Process) ที่ต้องถูกบันทึกเป็น First-class artifact

มาตรฐานนี้จะช่วยขจัด Scalability Bottleneck ในการพัฒนา Agentic Workflow โดยเฉพาะในช่วงการทำ SFT (Supervised Fine-tuning) และ RL (Reinforcement Learning) ซึ่งต้องการโครงสร้างที่รองรับการทดลองจำนวนมหาศาลโดยไม่สูญเสียความสามารถในการควบคุมคุณภาพ


--------------------------------------------------------------------------------


2. โครงสร้าง Repository และการจัดการโครงการ (Repository Structure & Organization)

เรากำหนดมาตรฐานโดยอิงจาก CCDS V2 และใช้ ccds CLI เป็นจุดเริ่มต้นของทุกโครงการ เพื่อสร้างโครงสร้างที่เป็นเอกภาพทั่วทั้งองค์กร

โครงสร้างโฟลเดอร์และ "So What?" Layer

โฟลเดอร์ / ไฟล์	หน้าที่สำคัญ	"So What?" Layer (ผลกระทบเชิงสถาปัตยกรรม)
data/	เก็บข้อมูล Raw, Intermediary, Processed	Immutable Raw Data: ป้องกันการปนเปื้อนของข้อมูลต้นฉบับ และใช้ DVC เพื่อหลีกเลี่ยง Git LFS bloat
models/	เก็บ Model Artifacts และ Registry Metadata	Traceability: เชื่อมโยงโมเดลเข้ากับ Experiment ID ป้องกัน Agent สับสนระหว่างรุ่นทดลองและรุ่นใช้งาน
notebooks/	สำหรับ EDA และการทดลองแบบ Sandbox	Namespace Protection: ป้องกันไม่ให้ Agent นำ Global variables จากการทดลองที่กระจัดกระจายเข้าไปใน Production code
{{module_name}}/	โค้ดหลักของระบบ (แทนที่ src/)	Package Integrity: ทำให้โปรเจกต์เป็น Python module ที่ติดตั้งได้ง่ายและมีโครงสร้างที่ชัดเจนสำหรับ CI/CD
pyproject.toml	การตั้งค่าโครงการและ Dependencies	Standardization: ใช้แทน setup.py เพื่อรองรับเครื่องมือสมัยใหม่ (เช่น uv, ruff) และประกาศ build-system ที่ชัดเจน
dvc.yaml	นิยาม Data Pipelines	Reproducibility: สร้าง DAG สำหรับการจัดการข้อมูลที่แยกออกจาก Source Control อย่างสมบูรณ์


--------------------------------------------------------------------------------


3. มาตรฐานการบันทึกการตัดสินใจทางสถาปัตยกรรม (Architectural Decision Records - ADR)

เราใช้มาตรฐาน MADR (Markdown Architectural Decision Records) รุ่น 3.0.0+ เพื่อบันทึกบริบท (Context) ของการตัดสินใจที่ส่งผลต่อระบบ

* Socio-technical Contract: ADR คือการ "Show your workings" เพื่อให้ทั้งมนุษย์และ AI Coding Agent เข้าใจเหตุผล (The "Why") เบื้องหลังโค้ด ป้องกันการแก้ไขโค้ดที่ขัดกับหลักการสถาปัตยกรรมที่วางไว้
* Naming Convention: NNNN-title-with-dashes.md (เช่น 0001-use-mlflow-for-tracking.md)
* MADR Full Template Structure: ต้องประกอบด้วย Context and Problem Statement, Decision Drivers, Considered Options, Decision Outcome และ Consequences (ซึ่งรวมผลกระทบเชิงบวกและลบเข้าด้วยกันตามมาตรฐานล่าสุด)


--------------------------------------------------------------------------------


4. การทำซ้ำและการบันทึกข้อมูลการทดลอง (Reproducibility & Logging)

ความโปร่งใสคือหัวใจของวิศวกรรม ML เรากำหนดมาตรฐานการบันทึกดังนี้:

* MLflow Autologging: ใช้ mlflow.autolog() เพื่อดึง Metrics และ Parameters อัตโนมัติ แต่สิ่งที่สำคัญที่สุดคือ Model Signatures (Input/Output Schemas) ซึ่งเปรียบเสมือนสัญญาที่ Agent ต้องใช้ในการสื่อสารกับ Model Artifact
* Environment Management: แนะนำให้ใช้ uv สำหรับความเร็วสูงสุดในการจัดการ Dependencies และสร้าง Lockfiles ที่แม่นยำ
* Reproducibility Checklist:
  * [ ] บันทึก Dataset Version (ผ่าน DVC Hash)
  * [ ] บันทึก Git Commit Hash ของโค้ดที่ใช้ในการรัน
  * [ ] บันทึก Model Signature เพื่อระบุ Interface ของโมเดล
  * [ ] บันทึก Software Environment (Lockfiles)


--------------------------------------------------------------------------------


5. สภาพแวดล้อมและการทำงานของ AI Coding Agent (AI Coding Agent Workflow & Safety)

การรันโค้ดที่สร้างโดย AI ต้องทำในสภาพแวดล้อมที่จำกัดสิทธิ์ (Isolated Runtime) ตามแนวทางของ Northflank และ SWE-World:

* MicroVM & Sandbox Isolation:
  * Ephemeral Execution: สำหรับงาน Tool calls หรือสคริปต์สั้นๆ ที่ต้องลบทิ้งทันทีเพื่อความปลอดภัย
  * Persistent Execution: สำหรับงานที่ต้องสะสม Context หรือ Artifacts โดยมีหน่วยความจำแยก (Attached Volumes)
* Learned Surrogate (SWE-World Model): สำหรับการ Scale การเทรนในระดับกว้าง เราใช้ Model-based environment:
  * SWT (Transition Model): ทำหน้าที่จำลองผลลัพธ์ของคำสั่ง Bash (stdout/stderr) เพื่อให้ Feedback ระดับขั้นตอนแก่ Agent โดยไม่ต้องรัน Docker จริง
  * SWR (Reward Model): ทำหน้าที่เป็น Virtual Test Runner เพื่อประเมินผลลัพธ์สุดท้ายและสร้าง structured test report
* Safety Constraints: กำหนดนโยบาย Default-deny networking และจำกัดทรัพยากร (Resource Limits) อย่างเข้มงวด ได้แก่ CPU, Memory, และ I/O caps ต่อหนึ่ง Session เพื่อป้องกัน "Runaway agents" ที่อาจทำลายโครงสร้างพื้นฐาน


--------------------------------------------------------------------------------


6. นโยบายการเปลี่ยนแปลงไฟล์และ Checklist การรวมระบบ (File-change Policy)

เพื่อให้ Agent ทำงานได้อย่างปลอดภัยและรักษาคุณภาพของ Codebase:

กฎเหล็กสำหรับการแก้ไขไฟล์ (File-change Policy):

1. Strict Diff Review: Agent ต้องใช้คำสั่ง diff เพื่อสรุปการเปลี่ยนแปลงก่อนส่งงานเสมอ
2. Docstring & Signature Update: ทุกครั้งที่มีการแก้ไข Function logic ต้องอัปเดต Docstring และ Type hints ให้ตรงกับพฤติกรรมจริง
3. Comment Preservation: ห้ามลบคอมเมนต์เดิมที่อธิบาย "เหตุผล" (Rationale) ของโค้ด เว้นแต่จะมีความจำเป็นเชิง Logic

Integration Checklist สำหรับ External Repos:

* [ ] Vulnerability Scanning: ตรวจสอบช่องโหว่ของ Dependencies ใหม่
* [ ] License Compliance: ตรวจสอบสิทธิ์การใช้งานของ Library ภายนอก
* [ ] F2P/P2P Verification: รันชุดทดสอบใน Sandbox ก่อนทำการ Merge


--------------------------------------------------------------------------------


7. ชุด Template มาตรฐานสำหรับวิศวกรรม (Standard Engineering Templates)

1. TEST_PLAN.md

# Test Plan: [Feature Name]
- **Objective:** [เป้าหมายการทดสอบ]
- **F2P (Fail-to-Pass) Tests:** [ลิสต์ Case ที่ต้องเปลี่ยนจากล้มเหลวเป็นผ่าน เพื่อยืนยันการแก้ Bug]
- **P2P (Pass-to-Pass) Tests:** [ลิสต์ Regression tests ที่ต้องผ่านเสมอเพื่อป้องกันผลกระทบย้อนกลับ]
- **Criteria:** [เกณฑ์การยอมรับ เช่น Resolve Rate > 90%]
- **Execution Env:** [Sandbox/MicroVM details]


2. EXPERIMENT_LOG.md

# Experiment Log: [ID]
- **Hypothesis:** [สมมติฐานการทดลอง]
- **Input Artifacts:** [DVC Data Hash, Base Model]
- **MLflow Run URL:** [Link ไปยัง Tracking Server]
- **Observations:** [ข้อสังเกตและพฤติกรรมอุบัติขึ้นที่พบ]


3. FAILURE_REPORT.md

# Failure Analysis Report
- **Issue Summary:** [สิ่งที่เกิดขึ้นจริงเทียบกับที่คาดหวัง]
- **Root Cause Analysis (RCA):** [สาเหตุหลักเชิงเทคนิค]
- **Agent Failure Mode:** [วิเคราะห์ว่า Agent ล้มเหลวในขั้นตอนใด (Navigation/Execution/Reasoning)]
- **Remediation:** [ขั้นตอนการแก้ไขและป้องกัน]


4. DECISION_RECORD.md (MADR 4.0.0 Full Template)

# [NNNN-title-with-dashes]

* Status: [proposed | accepted | superseded by [ADR-nnnn](ADR-nnnn.md) | ... ]
* Deciders: [list all involved]
* Date: [YYYY-MM-DD]

## Context and Problem Statement
[อธิบายบริบทและปัญหาที่ต้องการการตัดสินใจ]

## Decision Drivers
* [driver 1, e.g., ความเร็วในการประมวลผล]
* [driver 2, e.g., งบประมาณโครงสร้างพื้นฐาน]

## Considered Options
* [option 1]
* [option 2]

## Decision Outcome
Chosen option: "[option 1]", because [เหตุผลหลัก]

### Consequences
* Good: [ผลกระทบเชิงบวก]
* Bad: [ผลกระทบเชิงลบหรือความเสี่ยงที่ยอมรับ]

## Pros and Cons of the Options
### [option 1]
* Good, because [argument]
* Bad, because [argument]


5. DIFF_SUMMARY.md

# Diff Summary
- **Total Churn:** [จำนวนบรรทัดที่เพิ่ม/ลด]
- **Key Changes:** [สรุปการเปลี่ยนแปลงหลักสำหรับ Human reviewer]
- **Impacted Modules:** [ลิสต์ Module ที่ได้รับผลกระทบ]


6. RUNNER_INSTRUCTIONS.md

# Execution Guide
- **Prerequisites:** [e.g., `ccds` installed, `uv` sync]
- **Setup Command:** `make create_environment && make requirements`
- **Run Command:** `python {{module_name}}/train.py --config [path]`
- **Resource Limits:** [CPU: 4, RAM: 16GB, IO: 100MB/s]


7. RESULT.md

# Final Artifact Summary
- **Primary Metric:** [เช่น F1-score: 0.92]
- **Model Signature:** 
    - Inputs: [Schema description]
    - Outputs: [Schema description]
- **Deployment Path:** [Path ใน Model Registry]
- **SWR Report:** [สรุปผลจาก SWR Reward Model]



--------------------------------------------------------------------------------


8. โครงสร้างไฟล์และคำสั่งสำหรับ Codex (Proposed File Tree & Codex Instructions)

Proposed File Tree

.
├── pyproject.toml         # มาตรฐาน PEP 621
├── dvc.yaml               # Pipeline versioning
├── docs/
│   ├── decisions/         # ADR (MADR format)
│   │   └── 0000-use-markdown-architectural-decision-records.md
│   └── templates/         # 7 Standard Templates
├── {{module_name}}/       # โค้ดหลัก (แทนที่ src/)
├── tests/                 # F2P & P2P tests
├── notebooks/             # EDA (Excluded from production)
└── data/                  # จัดการผ่าน DVC


Codex Instructions (System Prompt)

"จงใช้ ccds CLI เพื่อ Initialize โปรเจกต์ใหม่ตามมาตรฐาน CCDS V2 โดยเปลี่ยนชื่อโฟลเดอร์ src/ ให้เป็นชื่อโปรเจกต์ สร้างไฟล์ pyproject.toml เริ่มต้นที่มีการตั้งค่า build-system และลบ setup.py ทิ้ง จากนั้นจงสร้างโฟลเดอร์ docs/decisions/ และวางไฟล์ 0000-use-markdown-architectural-decision-records.md ลงไป พร้อมทั้งสร้างไฟล์ Markdown templates ทั้ง 7 ชุดไว้ใน docs/templates/ ตามโครงสร้าง Engineering Standard Pack ที่ระบุไว้ในรายงานนี้"

บทสรุป: มาตรฐานนี้คือความมุ่งมั่นที่จะเปลี่ยนการทดลอง ML จาก "งานฝีมือ" ให้เป็น "วิศวกรรม" ที่เชื่อถือได้ การนำไปใช้อย่างเคร่งครัดจะช่วยลด Technical Debt และเพิ่มศักยภาพสูงสุดให้กับ AI Agent ในการทำงานร่วมกับมนุษย์อย่างยั่งยืน
