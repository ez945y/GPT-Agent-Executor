# GPT Agent Executor：實現自主協作與持續運行

# 專案內容

[English version](README_EN.md)

本專案旨在構建一個基於 GPT 的自主智能體框架，實現智能體的持續運行和協作。

通過模組化的設計，我們將智能體分解為三大核心模塊：

* **Think Agent（思考智能體）：** 負責分析目標、規劃任務和生成行動方案。
* **Tool Agent（工具智能體）：** 根據思考智能體的決策，調用外部工具或 API 執行具體任務。
* **Target Agent（目標智能體）：** 負責觀察自己的念頭，決定自己要做什麼的tool，會回傳一個target。

此外，本專案提供友好的使用者交互介面，並支援 Ollama 和 Gemini API 等多種語言模型後端，方便您根據需求選擇最適合的模型。

## 專案特色

* **自主運行：** 智能體能夠根據目標自主規劃和執行任務，無需人工干預。
* **模組化設計：** 三大核心模塊各司其職，方便擴展和維護。
* **多模型支援：** 支援 Ollama 和 Gemini API 等多種語言模型後端，靈活選擇。
* **使用者交互：** 提供友好的使用者交互介面，方便使用者與智能體互動。
* **持續學習：** 智能體能夠通過與環境互動不斷學習和進化。

## 專案架構

* **Think Agent：**
    * 負責目標分析、任務規劃、行動決策。
    * 利用語言模型生成思考過程和行動方案。
* **Tool Agent：**
    * 根據 Think Agent 的決策，調用外部工具或 API。
    * 負責執行具體任務，並將結果返回給 Think Agent。
* **Target Agent：**
    * 負責觀察自己的念頭，決定自己要做什麼的tool，會回傳一個target。
    * 將目標回傳給think agent。
* **使用者交互：**
    * 提供命令列介面或 Web 介面。
    * 允許使用者設定目標、查看進度、與智能體互動。
* **模型後端：**
    * 支援 Ollama 和 Gemini API。
    * 允許使用者根據需求選擇模型。

## 使用場景

* **自動化任務執行：** 自動執行資料收集、報告生成、程式碼編寫等任務。
* **智能助手：** 提供個人助理、客戶服務、知識問答等服務。
* **研究與開發：** 用於探索智能體行為、測試語言模型能力。

## 安裝

1.  **安裝 Conda：**
    * 如果您的電腦上還沒有安裝 Conda，請從 Anaconda 官方網站下載並安裝 Anaconda 或 Miniconda。
2.  **建立 Conda 環境：**
    * 使用以下命令建立 Conda 環境：
        * `conda create --name continuous-gpt-ai-agent --file requirements.txt`
    * 或者，您也可以使用以下命令從 `requirements.txt` 檔案建立環境：
        * `conda env create -f environment.yml`
3.  **啟用 Conda 環境：**
    * 使用以下命令啟用 Conda 環境：
        * `conda activate continuous-gpt-ai-agent`
4.  **執行專案：**
        * `python main.py`

## 未來展望

* 增加更多工具和 API 支援。
* 優化智能體的學習和推理能力。
* 開發更豐富的使用者交互介面。
* 探索多智能體協作。

## 貢獻指南

* 歡迎貢獻程式碼、文件、測試用例等。
* 請參考貢獻指南，瞭解如何參與專案。

## 授權條款

* 本專案採用 [授權條款名稱] 授權。