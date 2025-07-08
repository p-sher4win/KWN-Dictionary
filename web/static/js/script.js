let keyboardVisible = false;

const keyboard = new window.SimpleKeyboard.default({
    onChange: input => document.getElementById("devanagari_input").value = input,
    onKeyPress: button => {
        if (button === "{reset}" ){
            keyboard.clearInput()
            document.getElementById("devanagari_input").value = ""
        }
    },
    layout: {
        default: [
            "अ आ इ ई उ ऊ ऋ ऌ ए ॲ",
            "  ऐ ओ ऑ औ अं अः  ",
            "् ा ि ी ु ू ृ ॢ े ॅ",
            "  ै ो ॉ ौ ं ः  ",
            "क ख ग घ ङ च छ ज झ ञ",
            "ट ठ ड ढ ण त थ द ध न",
            "प फ ब भ म य र ऱ ल व",
            "  श ष स  ह ळ  ",
            "त्र  ज्ञ क्ष श्र   ँ ़ ।",
            "{reset} {space} {bksp}"
        ]
    },
    display: {
        "{bksp}": "⌫",
        "{space}": "____",
        "{reset}": "⟲"
    }
});

function toggleKeyboard() {
    keyboardVisible = !keyboardVisible;
    document.getElementById("keyboard").style.display = keyboardVisible ? "block" : "none";
}