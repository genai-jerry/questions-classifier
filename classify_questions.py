import pdfplumber
import re

# Functions

def is_derivation(question):
    return "derive" in question.lower()

def is_objective_type(question):
    patterns = [r'\(a\)', r'\(b\)', r'\(c\)', r'\(d\)']
    return all(re.search(pattern, question) for pattern in patterns)

def classify_chapter(question):
    keywords = {
        'Laws of Motion': ['newton', 'motion', 'friction', 'kinematics', 'dynamics'],
        'Work, Energy and Power': ['work', 'energy', 'power', 'potential', 'kinetic', 'conservation'],
        'Properties of Fluids': ['fluid', 'hydraulic', 'pneumatic', 'bernoulli', 'viscosity', 'buoyant'],
        'Thermodynamics': ['thermodynamics', 'enthalpy', 'entropy', 'heat', 'thermal', 'thermo', 'calorimetry'],
        'Wave Phenomena': ['wave', 'oscillat', 'vibration', 'resonance'],
        'Electric Charge and Electric Field': ['electric charge', 'electric field', 'coulomb'],
        'Electric Potential and Capacitors': ['electric potential', 'capacitor'],
        'Electric Current': ['current', 'resistor', 'ohm', 'circuit'],
        'Magnetism and Magnetic Effect': ['magnet', 'ferromagnetic', 'electromagnet'],
        'Electromagnetic Induction and PE Alternating Current': ['electromagnetic induction', 'alternating current', 'ac', 'emf'],
        'Dispersion and Scattering of light': ['dispersion', 'scattering', 'prism'],
        'Wave Phenomena and Light': ['diffraction', 'interference', 'polarization'],
        'Structure of Atom': ['atom', 'electron', 'proton', 'neutron', 'nucleus', 'orbital'],
        'Dual Nature of Radiation and Matter': ['photoelectric', 'compton', 'wave-particle duality', 'photon'],
        'Nuclei and Radioactivity': ['nuclei', 'radioactive', 'alpha', 'beta', 'gamma', 'half-life', 'decay'],
        'Nuclear Fission and Fusion': ['fission', 'fusion', 'chain reaction'],
        'Semiconductors and Semiconducting Devices': ['semiconductor', 'diode', 'transistor', 'n-type', 'p-type', 'pn junction'],
        'Applications of Semiconductor Devices': ['led', 'photodiode', 'solar cell', 'logic gate']
    }
    for chapter, keys in keywords.items():
        if all(key in question.lower() for key in keys):
            return chapter
    return "Unknown Chapter"

def extract_choices(question):
    choices_pattern = re.compile(r'\(a\).*?\(b\).*?\(c\).*?\(d\).*', re.DOTALL)
    match = choices_pattern.search(question)
    if match:
        return match.group()
    return None

import os
def process_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        total_pages = len(pdf.pages)
        for page_number in range(total_pages):
            try:
                page_text = pdf.pages[page_number].extract_text()
                if not page_text:
                    continue
            except:
                print(f'Encountered issue in {page_number}, continuing')
                continue

            page_lines = page_text.split('\n')
            question_pattern = re.compile(r'^\d+\.')

            page_questions = []
            current_question = ''

            for line in page_lines:
                if question_pattern.match(line):
                    if current_question:
                        page_questions.append(current_question.strip())
                    current_question = line
                else:
                    current_question += ' ' + line

            if current_question:
                page_questions.append(current_question.strip())

            for question in page_questions:
                q_text = question.split(' ')[1:]
                q_text = ' '.join(q_text)
                
                derivation = is_derivation(q_text)
                chapter = classify_chapter(q_text)

                # Only write derivation questions to the output
                if derivation:
                    with open('output.txt', 'a') as f:
                        f.write(f"{os.path.basename(file_path)} {file_path}\n")
                        f.write(f"{q_text}\n")
                        f.write(f"<Derivation={derivation}><Chapter Name: {chapter}>\n\n")
            print(f'Finished page number {page_number}')
    print(f'Completed reading file {file_path}')

# Main Script
# Main Script
def main():
    root_directory = "/home/jerrykurian/Downloads/NIOS/Physics/past_papers"  # current directory; update with the desired root directory path

    for subdir, dirs, files in os.walk(root_directory):
        for file in files:
            if file.endswith(".pdf"):
                file_path = os.path.join(subdir, file)
                print(f'Processing file {file_path}')
                process_pdf(file_path)

if __name__ == "__main__":
    main()




