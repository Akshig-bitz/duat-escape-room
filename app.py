from flask import Flask, render_template, request

app = Flask(__name__)

PASSCODE = "alohomora"

# Multiple acceptable villain spellings
VALID_VILLAINS = [
    "vader",
    "darth vader",
    "lord vader"
]

# Multiple acceptable spell variations
VALID_SPELLS = [
    "familia traumaticus",
    "familia-traumaticus",
    "familiatraumaticus"
]

REPAIR_CODE = "repairo_39"

MAX_ATTEMPTS = 2


@app.route("/", methods=["GET", "POST"])
def game():

    stage = 0
    attempts = 0
    error = None

    if request.method == "POST":
        stage = int(request.form.get("stage", 0))
        attempts = int(request.form.get("attempts", 0))

        # CASE-INSENSITIVE input
        villain_input = request.form.get("villain", "").strip().lower()
        spell_input = request.form.get("spell", "").strip().lower()
        single_input = request.form.get("input", "").strip().lower()

        # STAGE 0 — PASSCODE
        if stage == 0:
            if single_input == PASSCODE:
                stage = 1
                attempts = 0
            else:
                attempts += 1
                if attempts >= MAX_ATTEMPTS:
                    stage = -1
                else:
                    error = f"⚠ Attempts remaining: {MAX_ATTEMPTS - attempts}"

        # STAGE 1 — RULEBOOK
        elif stage == 1:
            stage = 2
            attempts = 0

        # STAGE 2 — VILLAIN + SPELL SAME PAGE
        elif stage == 2:
            if villain_input in VALID_VILLAINS and spell_input in VALID_SPELLS:
                stage = 3
                attempts = 0
            else:
                attempts += 1
                if attempts >= MAX_ATTEMPTS:
                    stage = -1
                else:
                    error = f"⚠ Attempts remaining: {MAX_ATTEMPTS - attempts}"

        # STAGE 3 — REPAIR CODE
        elif stage == 3:
            if single_input == REPAIR_CODE:
                stage = 4
            else:
                attempts += 1
                if attempts >= MAX_ATTEMPTS:
                    stage = -1
                else:
                    error = f"⚠ Attempts remaining: {MAX_ATTEMPTS - attempts}"

    return render_template(
        "game.html",
        stage=stage,
        attempts=attempts,
        error=error
    )


if __name__ == "__main__":
    app.run()
