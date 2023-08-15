def create_vcn(oci, network_composite_operations_virtual, comp_id, cidr_b, display_name):
    create_vcn_details = oci.core.models.CreateVcnDetails(
        cidr_blocks=cidr_b,
        display_name=display_name,
        compartment_id=comp_id
    )
    create_vcn_response = network_composite_operations_virtual.create_vcn_and_wait_for_state(
        create_vcn_details,
        wait_for_states=[oci.core.models.Vcn.LIFECYCLE_STATE_AVAILABLE]
    )
    created_vcn = create_vcn_response.data

    print('created_vcn: {}'.format(created_vcn))

    return created_vcn


def create_subnet(oci, network_composite_operations_virtual, virtual_cloud_network, availability_domain, display_name):
    create_subnet_details = oci.core.models.CreateSubnetDetails(
        compartment_id=virtual_cloud_network.compartment_id,
        availability_domain=availability_domain,
        display_name=display_name,
        vcn_id=virtual_cloud_network.id,
        cidr_block=virtual_cloud_network.cidr_block
    )
    create_subnet_response = network_composite_operations_virtual.create_subnet_and_wait_for_state(
        create_subnet_details,
        wait_for_states=[oci.core.models.Subnet.LIFECYCLE_STATE_AVAILABLE]
    )
    created_subnet = create_subnet_response.data

    print('Created Subnet: {}'.format(created_subnet))

    return created_subnet


def object_storage_limits(oci, config, comp_id):
    limits_client = oci.limits.LimitsClient(config)
    list_limit_values_response = limits_client.list_limit_values(comp_id, 'object-storage')
    print('Object storage limits: {}'.format(list_limit_values_response.data))


def create_compute_instance(oci, compute_composite_operations, compute_cl, compute_os, compute_shape, instance_name,
                            availability_domain, comp_id, ocpus, vcpus, subnet):
    list_images_response = oci.pagination.list_call_get_all_results(
        compute_cl.list_images,
        comp_id,
        operating_system=compute_os,
        shape=compute_shape
    )
    images = list_images_response.data

    # Get the first available image
    image = images[0]

    instance_source_via_image_details = oci.core.models.InstanceSourceViaImageDetails(
        image_id=image.id
    )

    create_vnic_details = oci.core.models.CreateVnicDetails(
        subnet_id=subnet.id
    )

    shape_config = oci.core.models.LaunchInstanceShapeConfigDetails(ocpus=ocpus,
                                                                    vcpus=vcpus)

    launch_instance_details = oci.core.models.LaunchInstanceDetails(
        display_name=instance_name,
        compartment_id=comp_id,
        availability_domain=availability_domain,
        shape=compute_shape,
        source_details=instance_source_via_image_details,
        create_vnic_details=create_vnic_details,
        shape_config=shape_config
    )

    launch_instance_response = compute_composite_operations.launch_instance_and_wait_for_state(
        launch_instance_details,
        wait_for_states=[oci.core.models.Instance.LIFECYCLE_STATE_RUNNING]
    )
    instance = launch_instance_response.data

    print('Created compute instance: {}'.format(instance))

    return instance


def destroy_compute_instance(oci, compute_composite_operations, compute_instance):
    compute_composite_operations.terminate_instance_and_wait_for_state(
        compute_instance.id,
        wait_for_states=[oci.core.models.Instance.LIFECYCLE_STATE_TERMINATED]
    )
    print('Terminated Compute Instance: {}'.format(compute_instance.id))

