from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from datetime import datetime
import json
import os

class WorkTracker(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Saugi failo lokacija Android sistemai
        self.data_dir = App.get_running_app().user_data_dir
        self.data_file = os.path.join(self.data_dir, "work_data_v2.json")

        self.data = self.load_data()
        self.update_labels()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                return json.load(f)
        return {}

    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.data, f)

    def save_hours(self):
        # Pasiimame ID reikšmes iš KV failo
        hours_input = self.ids.hours_input
        rate_input = self.ids.rate_input
        status_label = self.ids.status_label

        try:
            hours = float(hours_input.text)
            # Jei įkainis neįvestas, pagal nutylėjimą nustatome 0
            rate = float(rate_input.text) if rate_input.text else 0.0
            
            if hours <= 0 or rate < 0:
                raise ValueError
            status_label.color = (0.42, 0.85, 0.42, 1) # Žalia spalva sėkmei
            status_label.text = "Duomenys sėkmingai išsaugoti!"
        except ValueError:
            status_label.color = (0.9, 0.3, 0.3, 1) # Raudona klaidai
            status_label.text = "Klaida! Įveskite teisingus teigiamus skaičius."
            return

        today = datetime.now().strftime("%Y-%m-%d")
        month = datetime.now().strftime("%Y-%m")

        if month not in self.data:
            self.data[month] = {}

        # Duomenų struktūra saugo ir valandas, ir tos dienos įkainį
        if today in self.data[month]:
            self.data[month][today]["hours"] += hours
            # Jei įvedamas naujas įkainis, atnaujiname jį
            if rate > 0:
                self.data[month][today]["rate"] = rate
        else:
            self.data[month][today] = {"hours": hours, "rate": rate}

        self.save_data()
        self.update_labels()
        hours_input.text = ""
        # Įkainio laukelio neišvalome, kad vartotojui nereikėtų jo vesti kasdien iš naujo

    def update_labels(self):
        month = datetime.now().strftime("%Y-%m")
        history_container = self.ids.history_container
        history_container.clear_widgets() # Išvalome seną sąrašą prieš atnaujinant

        if month in self.data:
            days = len(self.data[month])
            total_hours = sum(item["hours"] for item in self.data[month].values())
            total_earnings = sum(item["hours"] * item.get("rate", 0) for item in self.data[month].values())
            
            # Generuojame istorijos įrašus (nuo naujausio iki seniausio)
            for date in sorted(self.data[month].keys(), reverse=True):
                day_data = self.data[month][date]
                h = day_data["hours"]
                r = day_data.get("rate", 0)
                
                # Sukuriame vizualią eilutę kiekvienam įrašui
                log_label = Label(
                    text=f"📅 {date}  |  [b]{h} val.[/b]  |  {r}€/h  (Viso: {h*r:.2f}€)",
                    font_size='14sp',
                    markup=True,
                    size_hint_y=None,
                    height='30dp',
                    halign='left',
                    text_size=(self.width - 40, None)
                )
                history_container.add_widget(log_label)
        else:
            days, total_hours, total_earnings = 0, 0, 0.0
            log_label = Label(text="Įrašų dar nėra", font_size='14sp', color=(0.5, 0.5, 0.5, 1))
            history_container.add_widget(log_label)

        # Atnaujiname pagrindinius skydelius
        self.ids.days_label.text = f"[b]{days}[/b]"
        self.ids.total_label.text = f"[b]{total_hours} val.[/b]"
        self.ids.earnings_label.text = f"[b]{total_earnings:.2f} €[/b]"


class WorkTrackerApp(App):
    def build(self):
        return WorkTracker()


if __name__ == "__main__":
    WorkTrackerApp().run()
