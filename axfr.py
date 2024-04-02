#!/bin/env python3

# Dependencies:
# python3-dnspython
import dns.zone as dz
import dns.query as dq
import dns.resolver as dr
import click

# Initialize Resolver-Class from dns.resolver as "NS"
NS = dr.Resolver()

# List of found subdomains
Subdomains = []

# Define the AXFR Function
def AXFR(domain, nameservers):

    # Try zone transfer for given domain and nameservers
    try:
        for nameserver in nameservers:
            # Perform the zone transfer
            axfr = dz.from_xfr(dq.xfr(nameserver, domain))

            # If zone transfer was successful
            if axfr:
                click.echo(f'[*] Successful Zone Transfer from {nameserver}')

                # Add found subdomains to global 'Subdomain' list
                for record in axfr:
                    Subdomains.append('{}.{}'.format(record.to_text(), domain))

    # If zone transfer fails
    except Exception as error:
        click.echo(error)
        pass

@click.command()
def main():
    # Get target domain
    domain = click.prompt('Please Enter the Target Domain', type=str)

    # Get nameservers
    nameservers_str = click.prompt('Please Enter the Name Servers Separated by commas', type=str)
    nameservers = nameservers_str.split(',')

    # Get output file name
    output_file = click.prompt('Please Enter the Output File Name (leave blank for no output file)', type=str, default='')

    # Call AXFR function
    AXFR(domain, nameservers)

    # Print or write the results
    if output_file:
        # Write to file
        with open(output_file, 'w') as f:
            for subdomain in Subdomains:
                f.write(subdomain + '\n')
        click.echo(f'Results written to {output_file}')
    else:
        # Print to terminal
        if Subdomains:
            click.echo('-------- Found Subdomains:')
            for subdomain in Subdomains:
                click.echo(subdomain)
        else:
            click.echo('No subdomains found.')

if __name__ == "__main__":
    main()
