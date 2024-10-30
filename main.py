from runoptions import (
    run_main,
    run_combined_hetro_plot,
    run_hetro_plot_detailed,
    run_hetro_plot_save_results,
    run_hetro_plot,
    run_main_plot,
    run_plot4dis_hetro,
    run_plot4dis_hetro_copy,
    run_prob36,
    run_temp_code_runner_file,
)

programs = {
    1: ("Start Heterogeneous Plot", run_hetro_plot.start_program),
    2: (
        "Start Hetrogeneous Plot and Save Results",
        run_hetro_plot_save_results.start_program,
    ),
    3: ("Start Heterogeneous Plot Detailed", run_hetro_plot_detailed.start_program),
    4: ("Start Main Simulation", run_main.start_program),
    5: ("Start Main Plot", run_main_plot.start_program),
    6: ("Start Plot for Distribution Heterogeneous", run_plot4dis_hetro.start_program),
    7: (
        "Start Plot for Distribution Heterogeneous Copy",
        run_plot4dis_hetro_copy.start_program,
    ),
    8: ("Start Probability 36", run_prob36.start_program),
    9: ("Start Temporary Code Runner", run_temp_code_runner_file.start_program),
    10: ("Start Combined Heterogeneous Plot", run_combined_hetro_plot.start_program),
}


def show_choices():
    print("Available Programs:")
    for key, (name, _) in programs.items():
        print(f"{key}: {name}")


def capture_choice():
    return input("\nEnter the number of the program you want to run (0 to exit): ")


def validate_choice(choice):
    try:
        choice = int(choice)
        if choice == 0:
            return 0
        elif choice in programs:
            return choice
        else:
            print("Invalid choice. Please try again.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None


def execute_choice(choice):
    print(f"\nStarting {programs[choice][0]}")
    programs[choice][1]()


def main():
    print("Starting simulation")

    while True:
        show_choices()
        user_choice = capture_choice()
        validated_choice = validate_choice(user_choice)

        if validated_choice == 0:
            break
        elif validated_choice is not None:
            execute_choice(validated_choice)
            break

    print("Finishing simulation")


if __name__ == "__main__":
    main()
