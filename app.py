from flask import Flask, render_template, request

app = Flask(__name__)

PASSCODE = "alohomora"

VALID_VILLAINS = [
    "vader",
    "darth vader",
    "lord vader"
]

VALID_SPELLS = [
    "familia traumaticus",
    "familia-traumaticus",
    "familiatraumaticus"
]

REPAIR_CODE = "repairo"

VALID_CREATORS = [
    "maat",
    "ma'at",
    "ma at"
]

MAX_ATTEMPTS = 2


@app.route("/", methods=["GET", "POST"])
def game():

    stage = 0
    attempts = 0
    error = None

    if request.method == "POST":
        stage = int(request.form.get("stage", 0))
        attempts = int(request.form.get("attempts", 0))

        user_input = request.form.get("input", "").strip().lower()
        villain_input = request.form.get("villain", "").strip().lower()
        spell_input = request.form.get("spell", "").strip().lower()
        repair_input = request.form.get("repair", "").strip().lower()
        creator_input = request.form.get("creator", "").strip().lower()

        # Stage 0 → Welcome → move to passcode
        if stage == 0:
            stage = 1

        # Stage 1 → Passcode
        elif stage == 1:
            if user_input == PASSCODE:
                stage = 2
                attempts = 0
            else:
                attempts += 1
                if attempts >= MAX_ATTEMPTS:
                    stage = -1
                else:
                    error = f"⚠ Attempts remaining: {MAX_ATTEMPTS - attempts}"

        # Stage 2 → Rulebook + Villain + Spell
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

        # Stage 3 → Repair + Creator
        elif stage == 3:
            if repair_input == REPAIR_CODE and creator_input in VALID_CREATORS:
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