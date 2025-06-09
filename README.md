# Anatra
**Anatra** is a command-line timer that tracks time with emoji-based categories and sends desktop notifications. Built currrently just for Windows.

```
         _.-.
    __.-' ,  \
   '--'-'._   \
           '.  \
            )   \ __.--._
           /   .'        '--.
          .               _/-._
          :       ____._/   _-'
           '._          _.'-'
              '-._    _.'
                  \_|/
                 __|||
                 >__/'
     ______                    __                     
    /\  _  \                  /\ \__                  
    \ \ \L\ \    ___      __  \ \ ,_\  _ __    __     
     \ \  __ \ /' _ `\  /'__`\ \ \ \/ /\`'__\/'__`\   
      \ \ \/\ \/\ \/\ \/\ \L\.\_\ \ \_\ \ \//\ \L\.\_ 
       \ \_\ \_\ \_\ \_\ \__/.\_\\ \__\\ \_\\ \__/.\_\
        \/_/\/_/\/_/\/_/\/__/\/_/ \/__/ \/_/ \/__/\/_/

```

🦆 Did you know? Ducks move gracefully in water, but what you don't see is how hard they're paddling underneath. From the surface, they look calm and effortless—yet below, they’re focused, active, and working with rhythm.

## Anatra Techinique 

like the duck, your productivity doesn’t have to look forced or rigid. It’s about finding your own rhythm —sometimes gliding, sometimes paddling— but always moving with intention. Anatra recognizes the work you put in, gives feedback when you need it, and reminds you that rewards come not from pushing harder, but from moving smarter.


## Compatibility
Anatra currrently just supports Windows.

## 🔧 Installation
### ✅ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/anatra.git
cd anatra
```

### ✅ Create and Activate a Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### ✅ Install Dependencies
```bash
pip install -r requirements.txt
```

### ✅ Install the CLI (Editable Mode)
```bash
pip install -e .
```

## 🚀 Usage
```bash
anatra <hours> <minutes> <seconds> <category> <emoji> <title>
```

## Examples
```bash
anatra 0 25 0 work 💻 "Code Website"
anatra 0 5 0 break ☕ "Coffee Break"
```

## Other Commands
```bash
anatra log        # Show log table
anatra -v         # Show version
anatra --help     # Show usage and options
```

# 📁 Project Structure
```
anatra/
├── anatra.py
├── setup.py
├── requirements.txt
├── .venv/                # Local virtual environment (not committed)
└── README.md
```
