# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: form_lib.pl,v 1.2 2000/12/14 01:17:02 oyvind Exp $


sub opt_prompt {
    my ($name) = ($_[0]);

#    my ($name, $length) = ($_[0], $_[1]);
    my $key = $name . '_opt';
  my $label =  $text{$key} ? $text{$key} : $key; 
    printf &hlink("<b>$label</b>", $name);
    
#    print "<input name=$name"."_def size=$length value=\"$v\"> </td>\n";


}
# option_radios_freefield(name_of_option, length_of_free_field, [name_of_radiobutton, text_of_radiobutton]+)
# builds an option with variable number of radiobuttons and a free field
# WARNING: *FIRST* RADIO BUTTON *MUST* BE THE DEFAULT VALUE OF POSTFIX
sub option_radios_freefield
{
    my ($name, $length) = ($_[0], $_[1]);

    my $v = &get_current_value($name);
    my $key = 'opts_'.$name;

    my $check_free_field = 1;
    
    printf "<td>".&hlink("<b>$text{$key}</b>", "opt_".$name)."</td> <td %s nowrap>\n",
    $length > 20 ? "colspan=3" : "";

    # first radio button (must be default value!!)
    
    printf "<input type=radio name=$name"."_def value=\"__DEFAULT_VALUE_IE_NOT_IN_CONFIG_FILE__\" %s> $_[2]\n",
    (&if_default_value($name)) ? "checked" : "";

    $check_free_field = 0 if &if_default_value($name);
    shift;
    
    # other radio buttons
    while (defined($_[2]))
    {
	printf "<input type=radio name=$name"."_def value=\"$_[2]\" %s> $_[3]\n",
	($v eq $_[2]) ? "checked" : "";
	if ($v eq $_[2]) { $check_free_field = 0; }
	shift;
	shift;
    }

    # the free field
    printf "<input type=radio name=$name"."_def value=__USE_FREE_FIELD__ %s>\n",
    ($check_free_field == 1) ? "checked" : "";
    printf "<input name=$name size=$length value=\"%s\"> </td>\n",
    ($check_free_field == 1) ? $v : "";
}


# option_freefield(name_of_option, length_of_free_field)
# builds an option with free field
sub option_freefield
{
    my ($name, $length) = ($_[0], $_[1]);

    my $v = &get_current_value($name);
    my $key = 'opts_'.$name;
    
    printf "<td>".&hlink("<b>$text{$key}</b>", "opt_".$name)."</td> <td %s nowrap>\n",
    $length > 20 ? "colspan=3" : "";
    
    print "<input name=$name"."_def size=$length value=\"$v\"> </td>\n";
}


# option_yesno(name_of_option, [help])
# if help is provided, displays help link
sub option_yesno
{
    my $name = $_[0];
    my $v = &get_current_value($name);
    my $key = 'opts_'.$name;

    defined($_[1]) ?
	print "<td>".&hlink("<b>$text{$key}</b>", "opt_".$name)."</td> <td nowrap>\n"
    :
	print "<td><b>$text{$key}</b></td> <td nowrap>\n";
    
    printf "<input type=radio name=$name"."_def value=\"yes\" %s> Yes\n",
    (lc($v) eq "yes") ? "checked" : "";

    printf "<input type=radio name=$name"."_def value=\"no\" %s> No\n",
    (lc($v) eq "no") ? "checked" : "";

    print "</td>\n";
}

1;
