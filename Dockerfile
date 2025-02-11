FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

WORKDIR /app

# Install git-lfs
RUN apt-get update && \
    apt-get install -y git-lfs && \
    git lfs install

# Configure conda to skip SSL verification
RUN conda config --set ssl_verify false

# Install dependencies using conda with --insecure flag
COPY requirements.txt .
RUN conda install -y --insecure -c conda-forge \
    omegaconf \
    torchaudio \
    einops \
    numpy \
    transformers \
    sentencepiece \
    tqdm \
    tensorboard \
    scipy=1.10.1 \
    accelerate && \
    PYTHONWARNINGS="ignore:Unverified HTTPS request" pip install --no-cache-dir \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    descript-audiotools>=0.7.2 \
    descript-audio-codec \
    runpod>=1.5.0 \
    huggingface-hub>=0.19.0 \
    flash-attn --no-build-isolation

# Copy local files
COPY . /app/YuE/inference/

# Get xcodec_mini_infer
RUN cd /app/YuE/inference && \
    GIT_SSL_NO_VERIFY=true git clone https://huggingface.co/m-a-p/xcodec_mini_infer

# Download model checkpoints with SSL verification disabled
ENV CURL_CA_BUNDLE=""
RUN python -c "from transformers import AutoModelForCausalLM; AutoModelForCausalLM.from_pretrained('m-a-p/YuE-s1-7B-anneal-en-cot', trust_remote_code=True); AutoModelForCausalLM.from_pretrained('m-a-p/YuE-s2-1B-general', trust_remote_code=True)"

WORKDIR /app/YuE/inference

CMD [ "python", "-u", "handler.py" ] 