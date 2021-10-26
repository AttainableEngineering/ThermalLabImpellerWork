from scipy.interpolate import interp1d
import matplotlib.pyplot as mp
import pandas as pd

def GetExpectedCurve():
    """
    Generate an impeller performance curve based on given parameters.
    """

    # Given Parameters
    H0 = 35         # [m]   -   Shutoff head
    a = -1600       # [s2/m5]   -   const
    b = 15          # [s/m2]    -   const
    n = 10          # [-]   -   blades
    Q_design = 0.08 # [m3/s]   -   design flowrate
    t = 3/16        # [in]
    t = t/39.37     # [m]
    RPM = 2500      # [rad/s]   -   design rpm
    
    # Generate Curve
    Head = []
    Flow = []
    for Q in range(0,10000):
        # Adjust Q below, and Range for resolution
        Q = Q/10000
        head = H0 + b*Q + a*(Q**2)
        if head < 0:
            # Stop iteration if negative
            break
        Head.append(head)
        Flow.append(Q)

    # Interpolate Values and return curve
    ExpectedCurve = interp1d(Flow, Head, kind="quadratic")

    return ExpectedCurve


def GetExperimentalCurve(fh = "ayayay.xlsx"):
    """
    Generate an impeller performance curve based on experimental results from Simerics CFD.\n
    Inputs:\n
    fh : file handle    -   str
    """

    try:
        # Open excel and pull columns of interest
        df = pd.read_excel(fh)
        # print(df)

        # Put data from excel into lists
        
        fcn = 'Q [m^3/s]' # Flow and head column names
        hcn = 'H [m]'
        exp_flow = df[fcn].tolist()
        exp_head = df[hcn].tolist()

        # Generate interpolation from excel data
        ExperimentalCurve = interp1d(exp_flow, exp_head, kind="quadratic")
        return ExperimentalCurve

    except Exception as er:
        # Error protection
        print("Error!" + str(er))
        

def CompareCurves(expected, experimental):
    """
    Compare two curves to determine correlation.\n
    Inputs:\n
    expected : expected curve value     -   interp1d\n
    experimental : experimental curve value     -   interp1d\n
    Outputs:\n
    TotalError : average percentage error between interpolations    -   float\n
    Valid : determines if the interpolation is within acceptable range  -   bool\n
    """

    # Find the error in every point of the interpolation
    errors = []
    act_list = []
    exp_list = []
    num_list = []
    for num in range(15200):
        # Sampling rate
        num = num/100000
        act = experimental(num)
        exp = expected(num)
        percent_error = abs( (act - exp) / exp)*100

        num_list.append(num)
        act_list.append(act)
        exp_list.append(exp)
        errors.append(percent_error)
    
    mp.plot(num_list, act_list, "o", num_list, exp_list)
    mp.legend(['Experimental Value', 'Expected Value'])
    mp.xlabel('Volumetric Flow Rate [m^3/s]')
    mp.ylabel('Head [m]')
    mp.xlim([0,.16])
    mp.ylim([0,38])
    mp.title("Experimental vs. Expected Performance Curve")

    # Get total error from average of the percent error at every point
    sum = 0
    count = 0
    for err in errors:
        sum += err
        count += 1
    TotalError = sum/count

    # Check if impeller is valid
    bounds = 15 # [%] maximum percent error
    if TotalError <= bounds:
        Valid = True
        print("\nThis impeller is valid.")
    else:
        Valid = False
        print("\nThis impeller is NOT valid.\n")

    return TotalError

if __name__ == "__main__":
    act = GetExpectedCurve()
    exp = GetExperimentalCurve()
    error = CompareCurves(act, exp)

    print("\nThe percentage error between data sets is:\n" + str(error) + "%\n")

    mp.show()