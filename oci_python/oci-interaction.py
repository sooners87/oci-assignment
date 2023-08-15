# example command: poetry run python .\oci_python\oci-interaction.py '10.0.0.0/16' 'vcn_test' 'subnet_test'
# 'instance-20230815-0235' 'VM.Standard.E2.1.Micro' 'Oracle Linux' 'wxDv:US-SANJOSE-1-AD-1' 1.0 2
import oci
from oci.config import from_file
from ociclientwrapper import create_vcn, create_subnet, create_compute_instance, object_storage_limits, \
    destroy_compute_instance
import sys

if __name__ == "__main__":
    if len(sys.argv) != 10:
        raise RuntimeError('Invalid number of arguments provided to the script.')

    cidr_blocks = [sys.argv[1]]  # ['10.0.0.0/16']
    vcn_name = sys.argv[2]  # 'vcn_test'
    subnet_name = sys.argv[3]  # 'subnet_test'
    instance_display_name = sys.argv[4]  # 'instance-20230815-0235'
    instance_shape = sys.argv[5]  # 'VM.Standard.E2.1.Micro'
    operating_system = sys.argv[6]  # 'Oracle Linux'
    availability_domain_name = sys.argv[7]  # 'wxDv:US-SANJOSE-1-AD-1'
    shape_config_ocpus = float(sys.argv[8])  # 1.0
    shape_config_vcpus = int(sys.argv[9])  # 2

    config = from_file()
    identity_client = oci.identity.IdentityClient(config)

    compute_client = oci.core.ComputeClient(config)
    compute_client_composite_operations = oci.core.ComputeClientCompositeOperations(compute_client)

    virtual_network_client = oci.core.VirtualNetworkClient(config)
    virtual_network_composite_operations = oci.core.VirtualNetworkClientCompositeOperations(virtual_network_client)

    compartment_id = config["tenancy"]

    vcn = create_vcn(oci, virtual_network_composite_operations, compartment_id, cidr_blocks, vcn_name)
    subnet = create_subnet(oci, virtual_network_composite_operations, vcn, availability_domain_name, subnet_name)

    # 1. Create a compute instance in OCI’s free tier.
    created_compute_instance = create_compute_instance(oci, compute_client_composite_operations, compute_client,
                                                       operating_system, instance_shape, instance_display_name,
                                                       availability_domain_name, compartment_id, shape_config_ocpus,
                                                       shape_config_vcpus, subnet)

    # 2. Query the OCI limits API to discover your free tier object storage limits.
    object_storage_limits(oci, config, compartment_id)

    # 3. Destroy the compute instance spun up.
    destroy_compute_instance(oci, compute_client_composite_operations, created_compute_instance)
