def available_zones(ec2):
    response = ec2.describe_availability_zones()
    availability_zones = response["AvailabilityZones"]
    available_zones = [
        zone for zone in availability_zones if zone["State"] == "available"
    ]
    return [name["ZoneName"] for name in available_zones]


def gpu_instance_types(ec2):
    paginator = ec2.get_paginator(
        ec2.get_instance_types_from_instance_requirements.__name__
    )
    page_iterator = paginator.paginate(
        ArchitectureTypes=["x86_64"],
        VirtualizationTypes=["hvm"],
        InstanceRequirements={
            "VCpuCount": {"Min": 1},
            "MemoryMiB": {"Min": 1},
            "InstanceGenerations": ["current"],
            "SpotMaxPricePercentageOverLowestPrice": 100,
            "OnDemandMaxPricePercentageOverLowestPrice": 20,
            "AcceleratorTypes": ["gpu"],
            "AcceleratorCount": {"Min": 1},
            "AcceleratorManufacturers": ["nvidia"],
            "AcceleratorNames": ["a100", "v100", "k80", "t4", "m60"],
        },
    )
    return [
        instance_type["InstanceType"]
        for page in page_iterator
        for instance_type in page["InstanceTypes"]
    ]


def spot_supported_instance_types(ec2, instance_types=[]):
    paginator = ec2.get_paginator(ec2.describe_instance_types.__name__)
    page_iterator = paginator.paginate(
        InstanceTypes=instance_types,
        Filters=[{"Name": "supported-usage-class", "Values": ["spot"]}],
    )
    return [
        instance_type["InstanceType"]
        for page in page_iterator
        for instance_type in page["InstanceTypes"]
    ]
