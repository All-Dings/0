# Dings-Backup-Makefile
#

## Backup-Dir
Backup_Dir := Backup

## Git_Sub_Module Number_Files
Number_File_List := $(wildcard *.*)

## Git_Sub_Module Number_Files without leading Directory
Number_File_List_Backup := $(notdir $(Number_File_List))
Number_File_List_Backup := $(addprefix $(Backup_Dir)/, $(Number_File_List))

## All_Rule
all: $(Backup_Dir) $(Number_File_List_Backup)

## Create Backup-Dir
$(Backup_Dir):
	if [ ! -d $(Backup_Dir) ] ; then mkdir $(Backup_Dir) ; fi

## Generate Backup-Files
$(Backup_Dir)/%: %
	cp $< $@

.PHONY: all
