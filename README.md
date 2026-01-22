# Formula E AI Selfie 🏎️📸

**Formula E AI Selfie** is a Generative Media demo that showcases the power of **Nano Banana Pro (Gemini 3 Flash Image Preview)** on Google Cloud's Vertex AI Platform.

This application allows users to take a selfie and seamlessly immerse themselves into the world of Formula E—transforming them into a race car driver, placing them on a track, or even turning them into a collectible figurine—all through the power of conversational image generation.

---

## 📖 Overview

The core technology behind this demo is the ability of Nano Banana Pro to handle **high quality conversational image generation** and **multiple reference images**.

By combining a user's uploaded selfie with reference images of the Formula E GenBeta car and specific branding, the model generates highly realistic, personalized output. It demonstrates how marketers and creatives can build personalized visual assets and immersive experiences.

### Key Features
*   **Selfie Integration:** Takes a participant's photo and blends it into a Formula E context.
*   **Reference Image Consistency:** Uses "few-shot" prompting with reference images (cars, logos), as well as Grounding with Google Search to ensure brand realism.
*   **Conversational Editing:** Users can refine the generated image by typing natural language edits (e.g., "Make the background sunny," "Add a helmet").
*   **Multi-Modal Inputs:** Handles text prompts and image inputs simultaneously.

---

## 🏗️ Architecture

The solution uses a serverless architecture on Google Cloud to ensure scalability and speed.

![Architecture Diagram](https://storage.googleapis.com/selfie-sample-images/formula_e_selfie_demo_architecture.svg)


### System Flow
1.  **Client (Frontend):** The user accesses a Web App hosted on **Firebase**. They capture a selfie and select a prompt theme.
2.  **Backend (Cloud Run):** The request is sent to a containerized Python service running on **Google Cloud Run**.
3.  **AI Processing (Vertex AI):** The Cloud Run service sends the selfie, prompt, and reference assets to **Nano Banana Pro (Gemini 3 Flash Image Preview)** via Vertex AI.
4.  **Generation & Storage:**
    *   The model edits the image into the themed setting.
    *   Cloud Run uploads the result to **Google Cloud Storage**.
5.  **Delivery:** A public URL is returned to the client, allowing the user to view, edit further, or scan a QR code to save the image.

---

## 🛠️ Technology Stack

*   **AI Model:** Gemini 3 Flash Image Preview ("Nano Banana Pro")
*   **Platform:** Google Cloud Vertex AI
*   **Backend:** Python (FastAPI)
*   **Compute:** Google Cloud Run
*   **Storage:** Google Cloud Storage
*   **Frontend Hosting:** Firebase

---

## 🚀 Getting Started

Follow these steps to deploy the backend service.

### Prerequisites
*   A Google Cloud Project with billing enabled.
*   Vertex AI API enabled.
*   Google Cloud CLI installed.
*   Python 3.9+.

### Local Development

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Reksmei/formula_e_selfie_backend.git
    cd formula_e_selfie_backend
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Environment Variables:**
    Create a `.env` file or export the following variables:
    ```bash
    export PROJECT_ID="your-gcp-project-id"
    export LOCATION="us-central1" # or your preferred region
    export BUCKET_NAME="your-gcs-bucket-name"
    ```

4.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```
    The server will start at `http://127.0.0.1:8000`.

### Deployment to Cloud Run

1.  **Build and Submit the Container:**
    ```bash
    gcloud builds submit --tag gcr.io/$PROJECT_ID/formula-e-backend
    ```

2.  **Deploy to Cloud Run:**
    ```bash
    gcloud run deploy formula-e-backend \
      --image gcr.io/$PROJECT_ID/formula-e-backend \
      --platform managed \
      --region us-central1 \
      --allow-unauthenticated \
      --set-env-vars PROJECT_ID=$PROJECT_ID,BUCKET_NAME=your-bucket-name
    ```

---

## 🔌 API Usage

The backend exposes endpoints to handle image generation.

### `POST /generate-image`

Uploads a selfie and generates a Formula E themed image.

*   **Headers:** `Content-Type: multipart/form-data`
*   **Body:**
    *   `file`: The user's selfie (image file).
    *   `prompt`: The text description (e.g., "Make me a driver on the track").
    *   `theme`: (Optional) The specific scenario ID.

---

## 💡 Potential Use Cases

While this demo focuses on Formula E fan engagement, the underlying "Nano Banana" technology has broad applications:

1.  **Retail & E-Commerce (Virtual Try-On):**
    *   Allow users to shop online and see how clothes suit them or a specific style before purchasing.
2.  **Architecture & Interior Design:**
    *   Merge multiple images and edit existing rooms. Designers can change furniture, colors, and layout using natural language.
3.  **Media & Entertainment:**
    *   Accelerate production timelines by visualizing storyboards. Turn rough sketches into realistic frames with high attention to detail.

---

## 📜 License

[MIT License](LICENSE)

---

**Disclaimer:** This is a demonstration project utilizing Google Cloud Vertex AI. Ensure you have the necessary quotas and permissions enabled in your Google Cloud project.
