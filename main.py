from run import SerialRunner
from formatter import Formatter
from saver import Saver


def run(simulation_name, file_name):
    runner = SerialRunner(simulation_name, 400, 1000)
    output = runner.run()

    formatter = Formatter(output)
    for_out = formatter.format()

    saver = Saver(for_out, file_name)
    saver.save()


def main():
    run("HamadryasSim", "hama_out.csv")
    run("SavannahSim", "sav_out.csv")


if __name__ == "__main__":
    main()
