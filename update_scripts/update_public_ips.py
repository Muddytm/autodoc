import pyconfluence as pyco
import skytap
from jinja2 import Template


def clean_name(name):
    """Clean name of environment."""
    return name.replace("+", "(and)").replace("/", "(slash)")


def start(envs, config_data):
    """Print all environments with public IPs to a page."""
    space = config_data["space"]
    other_docs_id = config_data["other_docs_id"]

    content = "Any and all environments with public IPs will be listed below.<br/>"

    with open("update_scripts/update_public_ips/public_ips.html", "r") as f:
        t = Template(f.read())

    for e in envs:
        vm_list = ""
        for v in e.vms:
            vm_found = False
            for i in v.interfaces:
                vm_hostname = i.hostname
                for p in i.public_ips:
                    vm_list += vm_hostname + ", "
                    vm_found = True
                    break
                if vm_found:
                    break
        if vm_list != "":
            content += t.render(name=clean_name(e.name), vm_list=vm_list[:-2])


    print content

    if content.strip() == pyco.get_page_content(pyco.get_page_id("Public IPs", space)).strip():
        print ("Content has not changed; skipping update.")
        return
    else:
        print pyco.edit_page(pyco.get_page_id("Public IPs", space), "Public IPs", space, content)
