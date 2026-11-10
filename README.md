

```markdown
# 🧠 CYBERBRAIN-1.1.0-45B-MoE
> **Unified Offline 6-Expert Dynamic Routing Engine for Autonomous Cybersecurity Intelligence**

[![Model Architecture](https://img.shields.io/badge/Architecture-6--Expert%20Multi--LoRA%20MoE-blue.svg)](#architecture--specifications)
[![Base Model](https://img.shields.io/badge/Base%20Backbone-Qwen2.5--Coder--7B--Instruct-brightgreen.svg)](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct)
[![Quantization](https://img.shields.io/badge/Quantization-BitsAndBytes%204--Bit%20NF4-orange.svg)](#hardware-requirements)
[![Environment](https://img.shields.io/badge/Platform-Windows%2011%20%7C%20Linux%20%7C%20CUDA-purple.svg)](#quickstart--setup)
[![License](https://img.shields.io/badge/License-Apache%202.0-red.svg)](LICENSE)

**CYBERBRAIN-1.1.0-45B-MoE** is a local, offline terminal CLI engine engineered for high-precision autonomous security auditing, protocol analysis, exploit assessment, and vulnerability triage. 

Instead of deploying a monolithic, hardware-prohibitive 40GB+ merged model, CYBERBRAIN leverages a **Dynamic Multi-LoRA Mixture-of-Experts (MoE)** routing topology. Powered by a single 4-bit NF4 quantized `Qwen2.5-Coder-7B-Instruct` backbone, it mounts 6 domain-specialized expert sub-brains simultaneously and switches between them at inference time with microsecond latency.

---

## 🏗 Architecture & Specifications

The engine separates domain knowledge into modular LoRA adapters while keeping a single unified base model in memory. The zero-overhead deterministic router inspects user intent and dynamically binds the corresponding specialized weights via `model.set_adapter()`.


```

```
                    ┌─────────────────────────────────────────┐
                    │        User Prompt / CLI Stream         │
                    └────────────────────┬────────────────────┘
                                         │
                              [ Intent Router / Gate ]
                                         │
  ┌──────────────┬──────────────┬────────┴─────┬──────────────┬──────────────┐
  ▼              ▼              ▼              ▼              ▼              ▼

```

┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ Phase 1  │   │ Phase 2  │   │ Phase 3  │   │ Phase 4  │   │ Phase 5  │   │ Phase 6  │
│Offensive │   │ Web/API  │   │  Binary  │   │  Cloud   │   │ Reasoning│   │ Protocol │
│  Core    │   │ Defense  │   │ Safety   │   │ Security │   │ Agentic  │   │ & Crypto │
└────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘
│              │              │              │              │              │
└──────────────┴──────────────┼──────────────┴──────────────┴──────────────┘
│  (Zero-Copy Adapter Switch)
┌───────────▼───────────┐
│   Qwen2.5-Coder-7B    │
│    (4-bit NF4 Base)   │
└───────────────────────┘

```

| Parameter | Specification |
| :--- | :--- |
| **Total Effective Capacity** | ~45B Domain Parameter Representation (Across 6 Trained Adapters) |
| **Base Core Model** | `Qwen/Qwen2.5-Coder-7B-Instruct` |
| **Quantization Scheme** | 4-bit NormalFloat4 (NF4) with Double Quantization via `bitsandbytes` |
| **Execution Framework** | PyTorch + Hugging Face Transformers + PEFT |
| **Memory Footprint** | ~5.5 GB – 6.2 GB VRAM (Full GPU Residency) |
| **Network Reliance** | 100% Offline (Zero external API / telemetry calls) |

---

## 🎯 The 6 Specialized Sub-Brains

CYBERBRAIN dynamically switches across six fine-tuned phases:

* **Phase 1: Offensive Core & Malware Reverse Engineering (`CYBERBRAIN_PHASE1`)**
  * Assembly analysis (x86_64/ARM), control-flow deobfuscation, shellcode evaluation, and reverse engineering heuristics.
* **Phase 2: Web Applications & API Security Auditing (`CYBERBRAIN_PHASE2`)**
  * Modern API auditing (REST/GraphQL), JWT/OAuth vulnerability detection, SSRF, IDOR, SQL injection, and web authentication boundary checking.
* **Phase 3: Binary Exploitation & Memory Safety (`CYBERBRAIN_PHASE3`)**
  * Stack/heap corruption, use-after-free triage, ROP/JOP chain verification, and mitigation bypasses (ASLR, DEP/NX, CFI).
* **Phase 4: Cloud & Container Infrastructure Defense (`CYBERBRAIN_PHASE4`)**
  * AWS/GCP/Azure IAM policy escalation paths, Kubernetes misconfigurations, Docker break-outs, and cluster isolation analysis.
* **Phase 5: Autonomous Reasoning & Strategic Planning (`CYBERBRAIN_PHASE5`)**
  * Multi-step autonomous decision making, chained attack surface modeling, adversary simulation, and root-cause post-mortem triage.
* **Phase 6: Protocol Dissection, Cryptography & RFC Auditing (`CYBERBRAIN_PHASE6`)**
  * Network packet parsing, custom Wireshark/Scapy dissector invariant verification, integer bounds checking, and cryptographic implementation scrutiny.

---

## 💻 Hardware Requirements

| Component | Minimum | Recommended |
| :--- | :--- | :--- |
| **GPU** | NVIDIA GPU with 6 GB VRAM (T4, RTX 3050, GTX 1660 Ti) | NVIDIA GPU with 8+ GB VRAM (RTX 3060/4060+) |
| **CUDA** | CUDA 11.8+ / 12.x | CUDA 12.1+ |
| **System RAM** | 8 GB RAM | 16 GB RAM |
| **Disk Space** | 20 GB (for base model weight cache & adapters) | Fast NVMe SSD |
| **OS** | Windows 10/11, Ubuntu 20.04+, WSL2 | Windows 11 / Linux |

---

## 🚀 Quickstart & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/safinulsafin0-byte/CYBERBRAIN-1.1.0-45B-MoE.git](https://github.com/safinulsafin0-byte/CYBERBRAIN-1.1.0-45B-MoE.git)
cd CYBERBRAIN-1.1.0-45B-MoE

```

### 2. Environment Setup & Dependencies

Ensure you have Python 3.10+ installed. Install the pinned dependencies:

```bash
pip install -r requirements.txt

```

### 3. Folder Layout for Local Adapters

Place your downloaded or trained adapter checkpoint directories inside your target model directory (e.g. `D:\CYBERBRAIN_MODELS` on Windows or `/home/user/CYBERBRAIN_MODELS` on Linux):

```text
D:\CYBERBRAIN_MODELS\
├── CYBERBRAIN_PHASE1/   <- adapter_model.safetensors, adapter_config.json
├── CYBERBRAIN_PHASE2/
├── CYBERBRAIN_PHASE3/
├── CYBERBRAIN_PHASE4/
├── CYBERBRAIN_PHASE5/
└── CYBERBRAIN_PHASE6/

```

---

## ⚡ Execution

Run the terminal interface by pointing to your adapter root directory:

#### On Windows (Command Prompt / PowerShell):

```cmd
python cyberbrain_cli.py --adapters "D:\CYBERBRAIN_MODELS"

```

#### On Linux / WSL2:

```bash
python cyberbrain_cli.py --adapters "/path/to/CYBERBRAIN_MODELS"

```

> **Note on Initial Run:** The script will download the base backbone (`Qwen/Qwen2.5-Coder-7B-Instruct`, ~15 GB) to your local Hugging Face cache once. Subsequent launches are strictly offline and load instantly from disk.

---

## 🎮 Interactive CLI Commands

Once initialized, the engine opens an interactive shell:

```text
CYBERBRAIN > Audit this C dissector: len = tvb_get_ntohl(tvb, 0); tvb_memcpy(tvb, buf, 4, len);

```

* `cls` or `clear`: Clears the terminal screen.
* `exit` or `quit`: Safely unloads adapters from VRAM and shuts down the engine.

---

## 🔒 Security & Safe Usage Disclaimer

CYBERBRAIN is designed strictly for authorized security auditing, academic research, reverse engineering, defensive validation, and boundary verification. Users are solely responsible for ensuring compliance with all local laws and target authorization policies.

```
