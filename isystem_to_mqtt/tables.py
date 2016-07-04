from ..tag_definition import TagDefinition, WriteTagDefinition
from . import convert

READ_TABLE = {
    231: TagDefinition("zone-a/program", convert.unit),
    507: TagDefinition("boiler/start-count", convert.unit_and_ten),
    509: TagDefinition("boiler/hours-count", convert.unit_and_ten),
    601: TagDefinition("outside/temperature", convert.tenth),
    602: TagDefinition("boiler/temperature", convert.tenth),
    607: TagDefinition("boiler/return-temperature", convert.tenth),
    610: TagDefinition("boiler/pressure", convert.tenth),
    614: TagDefinition("zone-a/temperature", convert.tenth),
    615: TagDefinition("zone-a/calculated-temperature", convert.tenth),
    620: TagDefinition("boiler/calculated-temperature", convert.tenth),
    650: TagDefinition("zone-a/day-target-temperature", convert.tenth),
    651: TagDefinition("zone-a/night-target-temperature", convert.tenth),
    652: TagDefinition("zone-a/antifreeze-target-temperature", convert.tenth)
}

WRITE_TABLE = {
    "zone-a/program/SET" : WriteTagDefinition(231, convert.write_unit), 
    "zone-a/day-target-temperature/SET" : WriteTagDefinition(650, convert.write_tenth),
    "zone-a/night-target-temperature/SET" : WriteTagDefinition(651, convert.write_tenth) 
}