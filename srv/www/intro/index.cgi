#!/usr/bin/env perl
use strict;
use warnings;

use CGI::Carp 'fatalsToBrowser';
use CGI ':standard';

sub get_level {
	my $ip = shift;

#	my $level = qx#/usr/local/lib/zensurbox/level_get $ip#;
	my $level = 0;

	my $exitstatus = $? >> 8;
	if ($exitstatus != 0) {
		die("Error getting level - script returned $exitstatus");
	}
	if ($level !~ /^ \d+ $/x) {
		die("Error getting level - returned level '$level' is not a digit");
	}

	return $level;
}

sub set_level {
	my ($ip, $level) = @_;
	
	if ($level !~ /^\d$/) {
		die("Invalid level");
	}

	qx#sudo /usr/local/lib/zensurbox/level_set $ip $level#;

	my $exitstatus = $? >> 8;
	if ($exitstatus != 0) {
		die("Error setting level - script returned $exitstatus");
	}

	return;
}

my $client_ip = $ENV{REMOTE_ADDR};
my $cgi = CGI->new();

# Die Aufgaben sind noch etwas out of date ;)
my $level = [
	{
		name => 'kein Level gewählt',
		task => 'Such dir ein Level aus :p',
	},
	{
		name => 'Leyenhaft',
		task => 'Lese aktuelle die Headline von blog.fefe.de vor',
	},
	{
		name => 'Beckstein',
		task => 'Informiere dich in der deutschen Wikipedia über das Tor-Netzwerk',
	},
	{
		name => 'Iran',
		task => 'Informiere dich über die Hommingberger Gepardenforelle',
	},
];


print "Content-type: text/html\n\n";

print <<'EOT';
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
	<title>Zensursulas Laptop</title>
	<meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
	<link rel="stylesheet" type="text/css" href="/keks.css"/>
	<base href="http://10.72.2.1" />
</head>
<body>
<div>
<h1>Zensursulas Laptop</h1>
<p class="intro"></p>
</div>
EOT

if (defined $cgi->param('set_level')) {
	set_level($client_ip, $cgi->param('set_level'));
	print "<div>Level updated. Please restart your browser.</div>\n";
}
else {
	print <<'EOT';
<div class="levelswitch">
<h1>Choose your censorship</h1>
EOT


	for my $cur_level (1 .. $#{$level}) {
		my $level_name = $level->[$cur_level]->{name};
		my $level_task = $level->[$cur_level]->{task};

		print "<div class=\"levelbox\">\n";
		print "<a href=\"index.cgi?set_level=$cur_level\"><img src=\"/levelicon/$cur_level.png\" alt=\"$level_name\"/></a><br/>\n";
		print "<p><a href=\"index.cgi?set_level=$cur_level\">Level $cur_level – $level_name</a></p>\n";
		print "<p>$level_task</p>\n";
		print "</div>\n";
	}

	print <<'EOT';
</div>
</body>
</html>
EOT
}
