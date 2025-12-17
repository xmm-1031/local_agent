# 智能文献与图像管理系统 README

## 1.项目简介

该项目是一个智能文献与图像管理系统，旨在通过自然语言处理和多模态技术来优化文献和图像的分类、检索和管理。用户可以上传论文，系统会自动进行语义分类并将文件归档至对应的子文件夹。同时，系统提供基于自然语言查询的文献语义搜索，可以迅速找到相关文献，并返回文献片段和页码。此外，系统还支持通过自然语言描述来搜索本地图像库中的图片。项目使用本地化部署。

## 2.核心功能
### 2.1 文献管理

语义搜索：支持使用自然语言提问（如“3DGS的原理是什么？”），系统基于语义理解返回最相关的论文文件，并能返回具体的论文片段或页码。
自动分类与整理：
单文件处理：添加新论文时，系统根据指定的主题（如 "3DGS,sparse view,network"）自动分析内容，并将论文归类并移动到对应的子文件夹。
批量整理：支持对现有的混乱文件夹进行“一键整理”，自动扫描所有 PDF，识别主题并归档到相应目录。
文件索引：支持基于语义向量进行文献搜索，快速定位所需文献，并能返回文献路径、主题和分数。

### 2.2 图像管理

以文搜图：支持通过自然语言描述（如“画画的小孩”）来查找本地图片库中最匹配的图像，使用图文匹配技术。

## 3.环境配置与依赖安装
### 3.1 安装 Python 依赖

该项目使用 Python 开发，建议使用虚拟环境来管理依赖，避免与系统环境发生冲突。
创建虚拟环境

python -m venv .venv

激活虚拟环境

Windows：.\.venv\Scripts\activate

Mac/Linux：source .venv/bin/activate

安装依赖
运行以下命令安装项目的所有依赖：

pip install -r requirements.txt

### 3.2 安装必要的软件包

PyMuPDF：用于从 PDF 中提取文
Sentence-Transformers：用于将文本转换为向量并进行语义搜索
ChromaDB：用于存储和查询向量数据库
Hugging Face Transformers：用于加载并使用预训练模型（如 CLIP）
你可以使用以下命令安装依赖：
pip install fitz sentence-transformers chromadb transformers

### 3.3 其他依赖

如果使用图像搜索功能，还需要安装相应的图像处理库（如 PIL 等）。

## 4.使用说明
### 4.1 启动系统
首先确保虚拟环境已经激活，并且安装了所有依赖。

### 4.2 向系统添加论文
通过命令行添加单个 PDF 文件，系统会根据文本内容自动分类并移动到对应子文件夹。
python main.py add_paper <paper_path> --topics "3DGS,sparse view,network"
<paper_path>：论文文件的路径。
--topics：一个或多个主题，用逗号分隔（如 "3DGS,sparse view,network"）。

### 4.3 批量整理文件夹中的论文
要整理文件夹中的所有 PDF 论文，并将它们根据主题进行分类，可以使用以下命令：
for %f in ("E:\local_agent\library\papers_raw\*.pdf") do python main.py add_paper "%f" --topics "3DGS,sparse view,network"
这条命令会批量处理 E:\local_agent\library\papers_raw\ 中的所有 PDF 文件，将它们按照指定的主题进行分类并移动到相应的子文件夹。

### 4.4 语义搜索文献
通过自然语言查询，系统可以基于论文内容返回最相关的文献，并显示相关片段和页码。
python main.py search_paper "3DGS的原理是什么？" --top_k 5 --show_snippet
--top_k：返回最相关的前 K 条结果。
--show_snippet：显示相关文献的片段。

### 4.5 以文搜图
通过自然语言描述，查询本地图像库中的最匹配图片：
python main.py search_image "画画的小孩" --top_k 5
--top_k：返回最相关的前 K 张图片。

### 4.6 技术选型说明                                    
1. 模型
Sentence-Transformers：使用 all-MiniLM-L6-v2 模型进行文本向量化，以便进行语义搜索。
CLIP：使用 openai/clip-vit-base-patch32 进行图文匹配，实现“以文搜图”的功能。

2. 数据库
ChromaDB：作为向量数据库，用于存储论文和图像的向量，支持高效的向量检索。

3. PDF 解析
PyMuPDF (fitz)：用于从 PDF 中提取文本，支持多种文本提取模式。

## 5.结语


该项目结合了自然语言处理、图像识别和向量数据库等技术，旨在实现更加智能和高效的文献与图像管理。通过该系统，用户可以快速对文献进行分类、检索，并且能够通过自然语言描述进行图像搜索。
