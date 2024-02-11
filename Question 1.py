import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import LANGUAGES, Translator

class LanguageTranslatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Language Translator")  # title of the application
        
        # Initializing translator object to get supported languages
        self.translator = Translator()
        self.languages = self.get_supported_languages()

        # Seting style theme
        self.style = ttk.Style(self)
        self.style.theme_use("clam")  # Changeable theme as preference
        
        # Create GUI widgets
        self.create_widgets()

    def create_widgets(self):
        # input field for text to translate
        self.label1 = ttk.Label(self, text="Enter text:")
        self.label1.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.input_text = tk.Text(self, height=5, width=40)
        self.input_text.grid(row=1, column=0, padx=5, pady=5)

        # Labels, dropdown, and buttons for language selection and translation
        self.label2 = ttk.Label(self, text="Select language to translate to:")
        self.label2.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.language_var = tk.StringVar()
        self.language_dropdown = ttk.Combobox(self, textvariable=self.language_var, values=self.languages)
        self.language_dropdown.grid(row=3, column=0, padx=5, pady=5)
        self.detect_button = ttk.Button(self, text="Detect Language", command=self.detect_language)
        self.detect_button.grid(row=3, column=1, padx=5, pady=5)
        self.translate_button = ttk.Button(self, text="Translate", command=self.translate_text)
        self.translate_button.grid(row=4, column=0, padx=5, pady=5)

        # output field for displaying translated text
        self.output_label = ttk.Label(self, text="Translated text:")
        self.output_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.output_text = tk.Text(self, height=5, width=40, state="disabled")
        self.output_text.grid(row=6, column=0, padx=5, pady=5)

    def detect_language(self):
        # Function to detect the language of input text
        text = self.input_text.get("1.0", "end-1c")
        
        if not text.strip():
            self.show_error("Please enter text for language detection.")
            return

        try:
            detected_lang = self.translator.detect(text).lang
            if detected_lang in LANGUAGES:
                self.show_info(f"Detected language: {LANGUAGES[detected_lang].capitalize()}")
            else:
                self.show_info("Language detected, but not supported.")
        except Exception as e:
            self.show_error(f"An error occurred during language detection: {str(e)}")

    def translate_text(self):
        # Function to translate input text to the selected language
        text = self.input_text.get("1.0", "end-1c")
        target_lang = self.language_var.get()

        if not text.strip():
            self.show_error("Please enter text to translate.")
            return

        if target_lang.lower() not in [lang.lower() for lang in LANGUAGES.values()]:
            self.show_error("Selected language is not supported.")
            return

        try:
            translated = self.translator.translate(text, dest=target_lang.lower()).text
            self.output_text.config(state="normal")
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", translated)
            self.output_text.config(state="disabled")
        except Exception as e:
            self.show_error(f"An error occurred during translation: {str(e)}")

    def get_supported_languages(self):
        # Function to get a list of supported languages
        supported_langs = sorted([LANGUAGES[lang].capitalize() for lang in LANGUAGES])
        return supported_langs

    def show_info(self, message):
        # Function to display information message
        messagebox.showinfo("Info", message)

    def show_error(self, message):
        messagebox.showerror("Error", message)

if __name__ == "__main__":
    # Create and run the application
    app = LanguageTranslatorApp()
    app.mainloop()
