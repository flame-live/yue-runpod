FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0

WORKDIR /app

# Install git-lfs
RUN apt-get update && \
    apt-get install -y git-lfs && \
    git lfs install

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install runpod flash-attn --no-build-isolation

# Copy local files
COPY . /app/YuE/inference/

# Get xcodec_mini_infer
RUN cd /app/YuE/inference && \
    git clone https://huggingface.co/m-a-p/xcodec_mini_infer

# Download model checkpoints
RUN python -c "from transformers import AutoModelForCausalLM; AutoModelForCausalLM.from_pretrained('m-a-p/YuE-s1-7B-anneal-en-cot'); AutoModelForCausalLM.from_pretrained('m-a-p/YuE-s2-1B-general')"

WORKDIR /app/YuE/inference

CMD [ "python", "-u", "handler.py" ] 