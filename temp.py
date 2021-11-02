specs_lookup_table = dict(
    BatterySpecs=dict(
        # lifetime
        lifetime_cycle="integer",
        lifetime_calendar="integer",
        lifetime_cycle_dod="floating",
        # chemestry
        # ChemestryCompatibility! min 1
        bess_chemestry_compatibility=enums['chemistry_compatibilities'],
        # electrical specs
        mean_efficiency="floating",
        # current
        max_charge="floating",
        nominal_charge="floating",
        max_discharge="floating",
        nominal_discharge="floating",
        # voltage
        max_voltage="floating",
        min_voltage="floating",
        nominal_voltage="floating",
        # capacity
        rated_Ah="floating",
        rated_kWh="floating"
    ),
    ControllerSpecs=None,
    EVChargerSpecs=dict(
        # lifetime
        lifetime_warranty="integer",
        applications=enums['applications'],
        # specs
        port_NB="integer",
        max_power_per_port_kW="floating",
        voltage_connections_main=enums['voltage_connections']
    ),
    InverterSpecs=dict(
        # AC
        # power
        max_power_kW="floating",
        nominal_power_kw="floating",
        # current
        peak_current="floating",
        peak_duration_seconds="integer",
        breaker_size="integer",
        max_continuous_current="floating",

        phases_NB="integer",
        # min 1
        voltage_connections=enums['voltage_connections'],
        frequency=enums['frequency'],
        active_frequency_shift_curtailment="boolean",
        # DC
        MPPT_NB="integer",
        max_power_per_MPPT_kW="floating",
        # current
        max_MPPT="floating",
        # max_MPPT2: Float
        # max_MPPT3: Float
        # max_MPPT4: Float
        # max_MPPT5: Float
        total_max="floating",
        usable_MPPT="floating",  # has to be the same number as max_MPPT
        # usable_MPPT2: Float
        # usable_MPPT3: Float
        # usable_MPPT4: Float
        # usable_MPPT5: Float
        # voltage
        MPPT_max_voltage="floating",
        MPPT_min_voltage="floating",
        nominal_voltage="floating",
        total_max_voltage="floating",
        operating_max_voltage="floating",
        operating_min_voltage="floating",
        # combiner boxes
        internal="boolean",
        string_number_limitation="integer",
        current_limitation="floating",

        lifetime_warranty="integer",
        grid_forming="boolean",
        CEC_efficiency="floating",
        MAX_efficiency="floating"
    ),
    InverterChargerSpecs=dict(
        lifetime_warranty="integer",
        grid_forming="boolean",
        UPS_function="boolean",
        # DC
        # current
        nominal_charge="floating",
        nominal_discharge="floating",
        max_charge="floating",
        max_discharge="floating",
        # voltage
        max_voltage_DC="floating",
        min_voltage_DC="floating",
        nominal_voltage_DC="floating",
        # chemistry min 1
        bess_chemestry_compatibility=enums['chemistry_compatibilities'],

        efficiency="floating",
        # AC
        nominal_power_kw="floating",
        # current
        peak_current="floating",
        nominal_current="floating",
        # voltage
        # min 1 connection
        voltage_connections=enums['voltage_connections'],
        max_voltage_AC="floating",
        min_voltage_AC="floating",
        nominal_voltage_AC="floating",

        frequency=enums['frequency']
    ),
    HybridInverterSpecs=dict(
        # general
        lifetime="integer",
        # min 1 connection
        voltage_connections=enums['voltage_connections'],
        grid_forming="boolean",
        external_MPPT="boolean",
        stacking_limit="integer",
        thee_phase_stacking="integer",
        UPS_function="boolean",
        # AC
        efficiency_AC="floating",
        nominal_power_kw="floating",
        # current
        peak_current="floating",
        nominal_current="floating",

        frequency=enums['frequency'],
        active_frequency_shift_curtailment="boolean",

        # solar(DC)
        MPPT_NB="integer",
        max_power_per_MPPT_kW="floating",
        # current
        max_MPPT1="floating",
        # max_MPPT2: Float
        # max_MPPT3: Float
        # max_MPPT4: Float
        # max_MPPT5: Float
        total_max="floating",
        usable_MPPT1="floating",  # has to be the same number as max_MPPT
        # usable_MPPT2: Float
        # usable_MPPT3: Float
        # usable_MPPT4: Float
        # usable_MPPT5: Float
        # voltage
        MPPT_max_voltage="floating",
        MPPT_min_voltage="floating",
        MPPT_nominal_voltage="floating",
        total_max_voltage="floating",
        operating_max_voltage="floating",
        operating_min_voltage="floating",
        # combiner boxes
        internal="boolean",
        string_number_limitation="integer",
        current_limitation="floating",

        # batteries
        # current
        nominal_charge="floating",
        nominal_discharge="floating",
        # voltage
        max_voltage="floating",
        min_voltage="floating",
        nominal_voltage="floating",
        # chemistry
        # min 1
        bess_chemestry_compatibility=enums['chemistry_compatibilities'],

        efficiency_DC="floating",
        max_capacity_kWh="floating",
        min_capacity_kWh="floating",
    ),
    MPPTSpecs=dict(
        # inverter dc up to grid forming - check again with Sam
        # DC
        MPPT_NB="integer",
        max_power_per_MPPT_kW="floating",
        # current
        max_MPPT1="floating",
        # max_MPPT2: Float
        # max_MPPT3: Float
        # max_MPPT4: Float
        # max_MPPT5: Float
        total_max="floating",
        usable_MPPT1="floating",  # has to be the same number as max_MPPT
        # usable_MPPT2: Float
        # usable_MPPT3: Float
        # usable_MPPT4: Float
        # usable_MPPT5: Float
        # voltage
        MPPT_max_voltage="floating",
        MPPT_min_voltage="floating",
        nominal_voltage="floating",
        total_max_voltage="floating",
        operating_max_voltage="floating",
        operating_min_voltage="floating",
        # combiner boxes
        internal="boolean",
        string_number_limitation="integer",
        current_limitation="floating",

        lifetime_warranty="integer",
        grid_forming="boolean"
    ),
    RapidShutdownSpecs=dict(
        RapidShutdownSpecs=dict(
            test_enums=enums['chemistry_compatibilities'],
            test_str="string",
            test_int="opt_integer",
            test_float="floating",
            test_bool="boolean"
        )
    ),
    SolarPanelSpecs=dict(
        lifetime_warranty="integer",
        # dimentions
        width_m="floating",
        length_m="floating",
        thickness_mm="floating",

        is_bifacial="boolean",
        # electrical specs
        IMP="floating",
        ISC="floating",
        VMP="floating",
        VOC="floating",
        NOCT="integer",
        NCell="integer",
        efficiency="floating",
        bifaial_gain="floating",
        temp_coeff_Isc="floating",
        temp_coeff_Voc="floating",
        temp_coeff_Pmax="floating",
        rated_power_stc_W="floating"
    )
)
