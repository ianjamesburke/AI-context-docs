# visual element format
tgb.visual_element_name("{variable}", param_1=param_1, param_2=param_2, ...)

# slider
tgb.slider("{variable}", min=min_value, max=max_value, ...)



# Examples

from taipy.gui import Gui
import taipy.gui.builder as tgb

if __name__ == "__main__":
    text = "Original text"

  with tgb.Page() as page:
      tgb.text("# Getting started with Taipy GUI", mode="md")
      tgb.text("My text: {text}")

      tgb.input("{text}")

  Gui(page).run(debug=True)

import taipy.gui.builder as tgb
from taipy.gui import Gui, notify
import taipy.gui.builder as tgb


def on_button_action(state):
    notify(state, 'info', f'The text is: {state.text}')
    state.text = "Button Pressed"

def on_change(state, var_name, var_value):
    if var_name == "text" and var_value == "Reset":
        state.text = ""
        return

if __name__ == "__main__":
    text = "Original text"

  # Definition of the page
  with tgb.Page() as page:
      tgb.text("# Getting started with Taipy GUI", mode="md")
      tgb.text("My text: {text}")

      tgb.input("{text}")
      tgb.button("Run local", on_action=on_button_action)

  Gui(page).run(debug=True)


list_to_display = [100/x for x in range(1, 100)]
with tgb.Page() as page:
    tgb.chart("{list_to_display}")





# table
with tgb.Page() as page:
    ...

  tgb.table("{dataframe}")
  tgb.chart("{dataframe}", type="bar", x="Text",
            y__1="Score Pos", y__2="Score Neu", y__3="Score Neg", y__4="Overall",
            color__1="green", color__2="grey", color__3="red", type__4="line")

dataframe = pd.DataFrame({"Text":['Test', 'Other', 'Love'],
                          "Score Pos":[1, 1, 4],
                          "Score Neu":[2, 3, 1],
                          "Score Neg":[1, 2, 0],
                          "Overall":[0, -1, 4]})

# Layput example
with tgb.Page() as page:
    with tgb.layout(columns="1 1"):
        with tgb.part():
            tgb.text("My text: {text}")
            tgb.input("{text}")
            tgb.button("Analyze", on_action=local_callback)

        with tgb.expandable("Table"):
            tgb.table("{dataframe}", number_format="%.2f")

    with tgb.layout(columns="1 1 1"):
        with tgb.part():
            tgb.text("## Positive", mode="md")
            tgb.text("{np.mean(dataframe['Score Pos'])}", format="%.2f")
        with tgb.part():
            tgb.text("## Neutral", mode="md")
            tgb.text("{np.mean(dataframe['Score Neu'])}", format="%.2f")
        with tgb.part():
            tgb.text("## Negative", mode="md")
            tgb.text("{np.mean(dataframe['Score Neg'])}", format="%.2f")

    tgb.chart("{dataframe}", type="bar", x="Text", y__1="Score Pos", y__2="Score Neu", y__3="Score Neg", y__4="Overall",
            color__1="green", color__2="grey", color__3="red", type__4="line")


# Page Selectors

from taipy import Gui
import taipy.gui.builder as tgb


def menu_option_selected(state, action, info):
    page = info["args"][0]
    navigate(state, to=page)

if __name__ == "__main__":
    # Add a navbar to switch from one page to the other
    with tgb.Page() as root_page:
        tgb.menu(label="Menu",
                lov=[('Page-1', 'Page 1'), ('Page-2', 'Page 2')],
                on_action=menu_option_selected)

        with tgb.Page() as page_1:
            tgb.text("## This is page 1", mode="md")
        with tgb.Page() as page_2:
            tgb.text("## This is page 2", mode="md")

        pages = {
            "/": root_page,
            "page1": page_1,
            "page2": page_2
        }
        Gui(pages=pages).run()





# Scenario
from taipy import Config
import taipy as tp
import taipy.gui.builder as tgb
import pandas as pd
import datetime as dt


data = pd.read_csv("https://raw.githubusercontent.com/Avaiga/taipy-getting-started-core/develop/src/daily-min-temperatures.csv")


# Normal function used by Taipy
def predict(historical_temperature: pd.DataFrame, date_to_forecast: dt.datetime) -> float:
    print(f"Running baseline...")
    historical_temperature["Date"] = pd.to_datetime(historical_temperature["Date"])
    historical_same_day = historical_temperature.loc[
        (historical_temperature["Date"].dt.day == date_to_forecast.day) &
        (historical_temperature["Date"].dt.month == date_to_forecast.month)
    ]
    return historical_same_day["Temp"].mean()

# Configuration of Data Nodes
historical_temperature_cfg = Config.configure_data_node("historical_temperature")
date_to_forecast_cfg = Config.configure_data_node("date_to_forecast")
predictions_cfg = Config.configure_data_node("predictions")

# Configuration of tasks
task_predict_cfg = Config.configure_task("predict",
                                        predict,
                                        [historical_temperature_cfg, date_to_forecast_cfg],
                                        predictions_cfg)

# Configuration of scenario
scenario_cfg = Config.configure_scenario(id="my_scenario",
                                         task_configs=[task_predict_cfg])

Config.export("config.toml")

if __name__ == "__main__":
    # Run of the Orchestrator
    tp.Orchestrator().run()

    # Creation of the scenario and execution
    scenario = tp.create_scenario(scenario_cfg)
    scenario.historical_temperature.write(data)
    scenario.date_to_forecast.write(dt.datetime.now())
    tp.submit(scenario)

    print("Value at the end of task", scenario.predictions.read())

    def save(state):
        state.scenario.historical_temperature.write(data)
        state.scenario.date_to_forecast.write(state.date)
        state.refresh("scenario")
        tp.gui.notify(state, "s", "Saved! Ready to submit")

    date = None
    with tgb.Page() as scenario_page:
        tgb.scenario_selector("{scenario}")
        tgb.text("Select a Date")
        tgb.date("{date}", on_change=save, active="{scenario}")

        tgb.text("Run the scenario")
        tgb.scenario("{scenario}")
        tgb.scenario_dag("{scenario}")

        tgb.text("View all the information on your prediction here")
        tgb.data_node("{scenario.predictions}")

    tp.Gui(scenario_page).run()
