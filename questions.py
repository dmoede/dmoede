QUESTIONS = [
    # --- Multiple Choice ---
    {
        "type": "mc",
        "question": "What does 'RAG' stand for in AI?",
        "options": ["A) Rapid Answer Generation", "B) Retrieval-Augmented Generation", "C) Recurrent Attention Graph", "D) Reinforced Agent Generation"],
        "answer": "B",
        "explanation": "RAG (Retrieval-Augmented Generation) combines a retrieval system with a generative model, letting it pull in real facts before answering — reducing hallucinations."
    },
    {
        "type": "mc",
        "question": "Which company created the Transformer architecture described in the famous 'Attention Is All You Need' paper?",
        "options": ["A) OpenAI", "B) Meta", "C) Google", "D) DeepMind"],
        "answer": "C",
        "explanation": "Google researchers published 'Attention Is All You Need' in 2017, introducing the Transformer — the architecture behind nearly every modern LLM."
    },
    {
        "type": "mc",
        "question": "What does 'RLHF' stand for?",
        "options": ["A) Reinforced Learning from Human Feedback", "B) Recursive Language from Hidden Features", "C) Reinforcement Learning from Human Feedback", "D) Ranked Learning with Hybrid Fine-tuning"],
        "answer": "C",
        "explanation": "RLHF (Reinforcement Learning from Human Feedback) is how models like ChatGPT are trained to be helpful and safe — humans rate outputs, and the model learns from those ratings."
    },
    {
        "type": "mc",
        "question": "What is a 'token' in the context of large language models?",
        "options": ["A) A security key used for API access", "B) A chunk of text (word, part of a word, or character) the model processes", "C) A single training example", "D) A reward signal used in reinforcement learning"],
        "answer": "B",
        "explanation": "Tokens are the basic units LLMs process — roughly 4 characters or 3/4 of a word on average. 'ChatGPT' is one token; 'unbelievable' might be split into two."
    },
    {
        "type": "mc",
        "question": "Which of these best describes 'hallucination' in AI?",
        "options": ["A) The model generates images from text", "B) The model confidently states false information", "C) The model refuses to answer a question", "D) The model runs too slowly"],
        "answer": "B",
        "explanation": "Hallucination is when an AI generates plausible-sounding but factually wrong information with confidence — a key challenge for LLMs."
    },
    {
        "type": "mc",
        "question": "What is 'fine-tuning' in machine learning?",
        "options": ["A) Adjusting hardware settings to speed up training", "B) Training a pre-trained model further on a specific dataset", "C) Removing parameters from a large model", "D) Adding more layers to a neural network"],
        "answer": "B",
        "explanation": "Fine-tuning takes a general pre-trained model and trains it further on domain-specific data, specializing it for a task without starting from scratch."
    },
    {
        "type": "mc",
        "question": "What company makes Claude?",
        "options": ["A) OpenAI", "B) Google", "C) Anthropic", "D) Meta"],
        "answer": "C",
        "explanation": "Claude is made by Anthropic, an AI safety company founded in 2021 by former OpenAI researchers including Dario Amodei and Daniela Amodei."
    },
    {
        "type": "mc",
        "question": "What does 'GPT' stand for?",
        "options": ["A) General Purpose Technology", "B) Generative Pre-trained Transformer", "C) Guided Probabilistic Training", "D) Graph Processing Toolkit"],
        "answer": "B",
        "explanation": "GPT stands for Generative Pre-trained Transformer. It describes the architecture: generative (produces text), pre-trained (on massive datasets), Transformer (the underlying architecture)."
    },
    {
        "type": "mc",
        "question": "What is 'prompt engineering'?",
        "options": ["A) Building hardware for AI training", "B) Writing software to generate prompts automatically", "C) Crafting inputs to get better outputs from AI models", "D) A method for compressing large models"],
        "answer": "C",
        "explanation": "Prompt engineering is the skill of writing and structuring inputs to AI models to get the best, most accurate, or most useful responses."
    },
    {
        "type": "mc",
        "question": "What is an 'embedding' in AI?",
        "options": ["A) Hiding secret data inside an image", "B) A numerical vector representation of text, images, or other data", "C) The process of compressing a model", "D) A type of activation function"],
        "answer": "B",
        "explanation": "Embeddings convert words, sentences, or images into lists of numbers (vectors) that capture meaning — similar concepts end up with similar numbers, enabling semantic search."
    },
    {
        "type": "mc",
        "question": "Which of these is NOT a large language model?",
        "options": ["A) Llama", "B) Gemini", "C) DALL-E", "D) Mistral"],
        "answer": "C",
        "explanation": "DALL-E is an image generation model made by OpenAI, not a language model. Llama (Meta), Gemini (Google), and Mistral are all LLMs."
    },
    {
        "type": "mc",
        "question": "What does 'context window' mean for an LLM?",
        "options": ["A) The size of the screen used during training", "B) The maximum amount of text the model can process at once", "C) A filter that removes harmful content", "D) The time limit for a single response"],
        "answer": "B",
        "explanation": "The context window is how much text (measured in tokens) a model can 'see' at once — both the input and its previous responses. Larger windows = longer conversations and documents."
    },
    {
        "type": "mc",
        "question": "What is 'temperature' in LLM settings?",
        "options": ["A) How fast the model runs", "B) The computing power used", "C) A setting that controls randomness in the model's output", "D) The length of the response"],
        "answer": "C",
        "explanation": "Temperature controls creativity vs. predictability. Low temperature (near 0) = consistent, focused answers. High temperature = more varied, creative, but potentially less accurate."
    },
    {
        "type": "mc",
        "question": "What company released the Gemini AI model family?",
        "options": ["A) Microsoft", "B) Apple", "C) Amazon", "D) Google"],
        "answer": "D",
        "explanation": "Google released Gemini in late 2023, positioning it as their answer to GPT-4. It's integrated into Google products like Search, Workspace, and Android."
    },
    {
        "type": "mc",
        "question": "What is 'model quantization'?",
        "options": ["A) Measuring a model's performance on benchmarks", "B) Reducing a model's precision to make it smaller and faster", "C) Adding more training data to improve accuracy", "D) A technique for combining multiple models"],
        "answer": "B",
        "explanation": "Quantization reduces the numerical precision of a model's weights (e.g., from 32-bit to 4-bit), making it much smaller and faster to run — key for running AI on phones and laptops."
    },
    {
        "type": "mc",
        "question": "Which technique lets a model reason step-by-step before giving a final answer?",
        "options": ["A) Zero-shot prompting", "B) Chain-of-thought prompting", "C) Retrieval augmentation", "D) Model distillation"],
        "answer": "B",
        "explanation": "Chain-of-thought (CoT) prompting encourages the model to show its reasoning steps before giving an answer, significantly improving accuracy on complex problems."
    },
    {
        "type": "mc",
        "question": "What does 'open source' mean when applied to an AI model?",
        "options": ["A) The model is free to use but code is private", "B) The model weights and/or code are publicly available", "C) The model can only be used for non-commercial purposes", "D) The model was trained on open internet data"],
        "answer": "B",
        "explanation": "Open source AI means the model weights (and often training code) are publicly released. Meta's Llama models are a prominent example — anyone can download and run them."
    },
    {
        "type": "mc",
        "question": "What is 'multimodal AI'?",
        "options": ["A) AI that runs on multiple computers at once", "B) AI that can process and generate more than one type of data (text, images, audio, etc.)", "C) AI trained on multiple languages", "D) AI that uses multiple algorithms simultaneously"],
        "answer": "B",
        "explanation": "Multimodal AI handles multiple data types. GPT-4o and Gemini are multimodal — they can understand images, audio, and text, not just text alone."
    },
    {
        "type": "mc",
        "question": "What is 'AI alignment'?",
        "options": ["A) Positioning AI servers in data centers efficiently", "B) Making sure AI models behave in ways that match human values and intentions", "C) Aligning different AI models to work together", "D) Training AI on balanced, unbiased datasets"],
        "answer": "B",
        "explanation": "AI alignment is the challenge of ensuring AI systems do what humans actually want and intend — not just what they're literally told. It's a central concern for AI safety researchers."
    },
    {
        "type": "mc",
        "question": "What does 'zero-shot' mean in AI?",
        "options": ["A) A model that has been trained with no data", "B) Running a model without any GPU", "C) Asking a model to do a task without any examples", "D) A model with zero errors"],
        "answer": "C",
        "explanation": "Zero-shot means asking a model to perform a task it wasn't explicitly trained for, with no examples provided — just a description. Powerful LLMs do this surprisingly well."
    },
    {
        "type": "mc",
        "question": "Which of these best describes 'AI agents'?",
        "options": ["A) Humans who train AI models", "B) AI systems that can take actions and complete multi-step tasks autonomously", "C) Software used to monitor AI systems", "D) A type of neural network layer"],
        "answer": "B",
        "explanation": "AI agents are systems that perceive their environment, plan, and take actions — like browsing the web, writing code, or sending emails — to complete goals with minimal human input."
    },
    {
        "type": "mc",
        "question": "What is 'model distillation'?",
        "options": ["A) Cleaning training data of harmful content", "B) Training a smaller model to mimic a larger one", "C) Removing duplicate data from training sets", "D) A method for detecting AI-generated text"],
        "answer": "B",
        "explanation": "Distillation trains a small, efficient 'student' model to replicate the behavior of a large 'teacher' model — you get most of the capability at a fraction of the compute cost."
    },
    {
        "type": "mc",
        "question": "ChatGPT was released publicly in what year?",
        "options": ["A) 2020", "B) 2021", "C) 2022", "D) 2023"],
        "answer": "C",
        "explanation": "ChatGPT launched on November 30, 2022, and reached 1 million users in just 5 days — the fastest product launch in history at the time."
    },
    {
        "type": "mc",
        "question": "What is 'Stable Diffusion'?",
        "options": ["A) A method for stabilizing AI training", "B) An open-source image generation AI model", "C) A technique for reducing LLM hallucinations", "D) A Google AI safety framework"],
        "answer": "B",
        "explanation": "Stable Diffusion is an open-source text-to-image AI model released by Stability AI in 2022. Because it's open source, it can be run locally on a personal computer."
    },
    {
        "type": "mc",
        "question": "What is a 'neural network' most inspired by?",
        "options": ["A) The structure of DNA", "B) The human brain's neurons and connections", "C) Mathematical graph theory", "D) Computer circuit boards"],
        "answer": "B",
        "explanation": "Neural networks are loosely inspired by biological brains — interconnected 'neurons' that pass signals and adjust connection strengths (weights) through learning."
    },

    # --- True / False ---
    {
        "type": "tf",
        "question": "True or False: An LLM 'knows' facts the same way a human knows facts — it stores them like a database lookup.",
        "answer": "False",
        "explanation": "LLMs don't store facts like a database. They compress patterns from training data into billions of weights. This is why they can 'know' something approximately but still hallucinate details."
    },
    {
        "type": "tf",
        "question": "True or False: GPT-4 was created by Google.",
        "answer": "False",
        "explanation": "GPT-4 was created by OpenAI, not Google. Google's equivalent frontier models are the Gemini family."
    },
    {
        "type": "tf",
        "question": "True or False: 'Parameters' in an LLM refer to the learned numerical weights that define the model's behavior.",
        "answer": "True",
        "explanation": "Parameters are the numbers adjusted during training. A model with 70 billion parameters has 70 billion individual numbers — each tuned to capture patterns in the training data."
    },
    {
        "type": "tf",
        "question": "True or False: AI models like ChatGPT are continuously learning from your conversations in real time.",
        "answer": "False",
        "explanation": "ChatGPT and similar models do NOT learn in real time from conversations. They have fixed weights after training. Your chat doesn't update the model — though companies may use feedback to train future versions."
    },
    {
        "type": "tf",
        "question": "True or False: 'Llama' is an open-source AI model family released by Meta.",
        "answer": "True",
        "explanation": "Meta's Llama (Large Language Model Meta AI) series is one of the most popular open-source LLM families. Developers worldwide use it to build applications without relying on OpenAI or Anthropic."
    },
    {
        "type": "tf",
        "question": "True or False: Bigger AI models are always better than smaller ones for every task.",
        "answer": "False",
        "explanation": "Larger models are generally more capable, but smaller specialized models often outperform large general models on specific tasks — and are much cheaper and faster to run."
    },
    {
        "type": "tf",
        "question": "True or False: The 'Transformer' architecture is the foundation of most modern LLMs, including GPT and Claude.",
        "answer": "True",
        "explanation": "Virtually every modern LLM is based on the Transformer architecture from the 2017 'Attention Is All You Need' paper. The attention mechanism lets the model weigh the relevance of every word to every other word."
    },
    {
        "type": "tf",
        "question": "True or False: An AI model with a larger context window can read and respond to longer documents.",
        "answer": "True",
        "explanation": "A larger context window means the model can process more text at once. Claude 3, for example, has a 200,000-token context window — enough to read an entire book."
    },
    {
        "type": "tf",
        "question": "True or False: 'Deepfakes' are created exclusively using generative AI.",
        "answer": "False",
        "explanation": "While modern deepfakes heavily use AI (GANs, diffusion models), early deepfakes used simpler video-editing techniques. The term doesn't require generative AI specifically."
    },
    {
        "type": "tf",
        "question": "True or False: OpenAI is a fully non-profit organization.",
        "answer": "False",
        "explanation": "OpenAI started as a non-profit in 2015 but created a 'capped-profit' subsidiary in 2019 to attract investment. It has since moved further toward a for-profit structure."
    },
    {
        "type": "tf",
        "question": "True or False: AI can currently pass the bar exam (the US lawyer licensing test).",
        "answer": "True",
        "explanation": "GPT-4 passed the bar exam in 2023, scoring around the 90th percentile. This was a landmark demonstration of LLM capability on professional certification tests."
    },
    {
        "type": "tf",
        "question": "True or False: 'Diffusion models' are the main technology behind modern text-to-image AI like Midjourney and DALL-E.",
        "answer": "True",
        "explanation": "Diffusion models work by learning to reverse a process of adding noise to images. At generation time, they start from random noise and gradually 'denoise' it into a coherent image."
    },
    {
        "type": "tf",
        "question": "True or False: AI models can be biased because of biases present in their training data.",
        "answer": "True",
        "explanation": "AI models learn patterns from training data. If that data reflects historical biases (racial, gender, cultural), the model can reproduce and even amplify those biases in its outputs."
    },
    {
        "type": "tf",
        "question": "True or False: 'AGI' (Artificial General Intelligence) has already been achieved.",
        "answer": "False",
        "explanation": "AGI — AI that matches or exceeds human-level intelligence across all domains — has not been achieved. Current AI is 'narrow': excellent at specific tasks but lacking general reasoning and adaptability."
    },
    {
        "type": "tf",
        "question": "True or False: Sam Altman is the CEO of Anthropic.",
        "answer": "False",
        "explanation": "Sam Altman is the CEO of OpenAI. Anthropic's CEO is Dario Amodei, who co-founded the company with his sister Daniela Amodei (President) after leaving OpenAI."
    },
    {
        "type": "tf",
        "question": "True or False: 'Few-shot prompting' means giving the model a few examples of the task inside the prompt.",
        "answer": "True",
        "explanation": "Few-shot prompting includes 2-5 examples of input→output pairs in the prompt itself. This dramatically improves performance on structured tasks without any retraining."
    },
    {
        "type": "tf",
        "question": "True or False: AI-generated text can always be detected by specialized software.",
        "answer": "False",
        "explanation": "AI detection tools exist but are unreliable — they produce both false positives (flagging human writing as AI) and false negatives (missing AI text). No tool reliably detects AI content."
    },
    {
        "type": "tf",
        "question": "True or False: 'Overfitting' means a model performs well on training data but poorly on new, unseen data.",
        "answer": "True",
        "explanation": "Overfitting happens when a model memorizes training examples instead of learning generalizable patterns. It 'cheats' on training data but fails on anything new."
    },
    {
        "type": "tf",
        "question": "True or False: Microsoft has made major investments in OpenAI.",
        "answer": "True",
        "explanation": "Microsoft has invested over $13 billion in OpenAI and integrated its technology deeply into products like Bing, Copilot, Azure, and Office 365."
    },
    {
        "type": "tf",
        "question": "True or False: The term 'machine learning' and 'artificial intelligence' mean exactly the same thing.",
        "answer": "False",
        "explanation": "AI is the broader field of making machines intelligent. Machine learning is a subset of AI focused on systems that learn from data. All ML is AI, but not all AI is ML."
    },
    {
        "type": "tf",
        "question": "True or False: 'Attention' in the Transformer architecture lets the model focus on relevant parts of the input when generating each output token.",
        "answer": "True",
        "explanation": "The attention mechanism is the key innovation of Transformers — it lets each word 'attend' to (consider) all other words simultaneously, capturing long-range relationships in text."
    },
    {
        "type": "tf",
        "question": "True or False: You need a PhD to build applications using AI APIs like Claude or GPT.",
        "answer": "False",
        "explanation": "Modern AI APIs are designed for mainstream developers — and even non-developers using tools like Claude Code. No advanced math or AI expertise is required to build powerful AI applications."
    },
    {
        "type": "tf",
        "question": "True or False: 'MCP' stands for Model Context Protocol, a standard for connecting AI models to external tools.",
        "answer": "True",
        "explanation": "MCP (Model Context Protocol) is an open standard created by Anthropic that lets AI assistants connect to external tools, databases, and services in a standardized way."
    },
]
