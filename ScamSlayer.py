import tkinter as tk
from tkinter import font, ttk
from PIL import Image, ImageTk  # Import PIL library for image resizing
import openai

openai.api_key = '[REDACTED]'

# Chatlog
chatlog = [
    {"role": "system", "content": "You are a chatbox designed to detect if an email is either Non-Malicious, suspicious, or malicious. Give it a confidence level from 1% to 100%. The output should look like Category(% Confidence)"},
    {"role": "system", "content": "Make sure to check for spelling mistakes, time limits given, suspicious links and if there are links, make sure that they are secure with SSL encryption, scare tactics, generic greetings, requests for personal information, or suspicious attachements"},
    {"role": "system", "content": "Make sure to answer in one word ONLY (Non-Malicious, Suspicious, or Malicious) and explain why in 3 short bullet points under 15 words."},
    {"role": "system", "content": "Do not include any explanation after the bullet points and DO NOT GO OVER 15 words."}
]

def submit():
    entered_text = text_entry.get("1.0", tk.END)
    entered_text = entered_text.strip()
    
    if entered_text:
        chatlog.append({"role": "user", "content": entered_text})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chatlog
        )

        response = completion.choices[0].message.content
        response_lines = response.split('\n')
        
        # Clear response and insert new
        result_text.delete(1.0, tk.END)
        
        for line in response_lines:
            result_text.insert(tk.END, line + "\n")

        # Memory
        chatlog.append({"role": "assistant", "content": response})

window = tk.Tk()
window.title("Scam Slayer")

window.geometry("800x600")

bg_color = "#FFFFFF"
fg_color = "#000000"
button_color = "#B0E0E6"

custom_font = font.Font(family="source-sans-pro", size=12, weight="bold")

window.configure(bg=bg_color)

image_path = "logo.png"  
original_image = Image.open(image_path)
resized_image = original_image.resize((180, 150), Image.ANTIALIAS)
tk_image = ImageTk.PhotoImage(resized_image)

# Display the image
image_label = tk.Label(window, image=tk_image, bg=bg_color)
image_label.pack(pady=10)

label = tk.Label(window, text="Enter your email text:", font=custom_font, bg=bg_color, fg=fg_color)
label.pack(pady=10)

# Text box
text_entry = tk.Text(window, height=15, width=65, font=custom_font, bg="#F0F0F0", fg=fg_color)
text_entry.pack(pady=10)

# Button
style = ttk.Style()
style.configure("TButton", padding=(10, 5, 10, 5), font=custom_font, background=button_color)
submit_button = ttk.Button(window, text="Submit", command=submit, style="TButton")
submit_button.pack()

result_text = tk.Text(window, height=20, width=65, font=custom_font, bg="#E6E6E6", fg=fg_color)
result_text.pack(pady=10)

window.mainloop()
