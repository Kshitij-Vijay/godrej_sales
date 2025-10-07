from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration,BlipForQuestionAnswering
from analyser.ollama_clients import *
from langchain_ollama import OllamaLLM

def blip_summarize_image(image_path):
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    out = model.generate(**inputs, max_length=30)
    caption = processor.decode(out[0], skip_special_tokens=True)  # decode first tensor only
    return caption

def blip_detailed_description(image_path,mini):
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    out = model.generate(
        **inputs,
        min_length = mini,
        max_length=200,      # Longer output for more details
        num_beams=20,         # Beam search for quality
        early_stopping=True  # Stop when sentence is complete
    )
    description = processor.decode(out[0], skip_special_tokens=True)
    return description

def blip_vqa(image_path, question):
    processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
    model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, question, return_tensors="pt")
    out = model.generate(**inputs)  # Use generate() for inference
    answer = processor.decode(out[0], skip_special_tokens=True)
    return answer


# questions = ["What color is the bed?","what is the main object in the picture?","How big is the bed ?","What does this picture indicate?"]


def blip_image_text(img_path, questions):
    qa_pairs = []
    for q in questions:
        answer = blip_vqa(img_path, q)
        qa_pairs.append(f"Q: {q}\nA: {answer}")

    short_desc = blip_summarize_image(img_path)
    qa_pairs.append(f"Q: short description\nA: {short_desc}")

    long_desc = blip_detailed_description(img_path, mini=50)
    qa_pairs.append(f"Q: long description\nA: {long_desc}")

    combined_text = "\n\n".join(qa_pairs)

    # llm = choose_model(model_type="llm")
    # print(llm)
    llm = OllamaLLM(model="smollm2:latest")


    prompt = "This are a few questions and answers : "+combined_text+" \n give me a summary of it without missing a single detail."

    response = llm.generate([prompt])
    answer = response.generations[0][0].text
    print("\nAnswer:\n" + answer + "\n")

    out = { "qna" : combined_text, "summary" : answer}

    return out

# print(blip_image_text("Screenshot 2025-09-13 110320.jpg",questions))

    

# image_path = "Screenshot 2025-09-13 110320.jpg"
# question = "What color is the bed?"
# print(blip_vqa(image_path, question))
# question = "what is the main object in the picture?"
# print(blip_vqa(image_path, question))
# question = "How big is the bed ?"
# print(blip_vqa(image_path, question))
# question = "What does this picture indicate?"
# print(blip_vqa(image_path, question))



# print(blip_summarize_image("56101515SD00062_Feature_03_680x600.jpg"))
# print(blip_detailed_description("56101515SD00062_Feature_03_680x600.jpg",100))