""" File that contains the DiffusionTensor class. """

# ##############################################################################
# Imports
# ##############################################################################

import molecular_dynamics.main.molecule as molecule

# ##############################################################################
# Main Function
# ##############################################################################


def main() -> None:
    """
        Runs the main program.
    """
    pnb = molecule.Molecule()

    print(str(pnb))

# ##############################################################################
# Main Program
# ##############################################################################


if __name__ == "__main__":
    """
        Runs the program.
    """
    main()
