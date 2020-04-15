from apa102_pi.colorschemes import colorschemes

num_leds = 180

def main():

    rainbow_cycle = colorschemes.Rainbow(num_led=num_leds, pause_value=0, num_steps_per_cycle=255, num_cycles=2)

    #rainbow_cycle.start()

    down_cycle = colorschemes.RoundAndRound(num_led=num_leds, pause_value=0.05, num_steps_per_cycle=num_leds, num_cycles=10)

    down_cycle.start()

    theater_cycle = colorschemes.TheaterChase(num_led=num_leds, pause_value=0.04, num_steps_per_cycle=255, num_cycles=10)

    #theater_cycle.start()

    print("Finished with the cycle")

main()