<?php

//returns a big old hunk of JSON from a non-private IG account page.
function scrape_insta($username) {
	$insta_source = file_get_contents('http://instagram.com/'.$username);
	$shards = explode('window._sharedData = ', $insta_source);
	$insta_json = explode(';</script>', $shards[1]);
	$insta_array = json_decode($insta_json[0], TRUE);
	return $insta_array;
}

//read in users from cleaned_users.txt
$accounts = array();
$accounts_file = fopen('users.txt', 'r');
if( $accounts_file == false) {
	echo ( "Error opening user file" );
	exit();
}
while(!feof($accounts_file)) {
	$line = fgets($accounts_file);
	$user = trim($line);
	array_push($accounts, $user);
}

$myfile = fopen("scraped2.csv", "w") or die("Unable to open file!");
$header = "img_url,img_caption,img_desc\n";
// only write header if the file is empty
//fwrite($myfile, $header);

//Do the deed
foreach ($accounts as &$my_account) {
	$results_array = scrape_insta($my_account);

	//An example of where to go from there
	$nodes = $results_array['entry_data']['ProfilePage'][0]['user']['media']['nodes'];

	for ($i = 0; $i < sizeof($nodes); $i++){
		// if there is no caption, continue
		try {
			$caption = $nodes[$i]['caption'];
		} catch (Exception $e) {
			continue;
		}
		//----- clean caption -----//
		// remove newlines and return characters
		$caption = str_replace("\n", ' ', $caption);
		$caption = str_replace("\r", ' ', $caption);
		$caption = str_replace("\r\n", ' ', $caption);
		// remove quotation marks and commas as those mess up the CSV
		$caption = str_replace(",", '', $caption);
		$caption = str_replace("\"", ' ', $caption);
		$url = $nodes[$i]['display_src'];
		// format data
		$data = "\"".$url."\",\"".$caption."\",\n";
		echo $data;
		fwrite($myfile, $data);
	}
}

fclose($myfile);
fclose($accounts_file);

//$latest_array = $results_array['entry_data']['ProfilePage'][0]['user']['media']['nodes'][0];

//echo 'Latest Photo:<br/>';
//echo '<a href="http://instagram.com/p/'.$latest_array['code'].'"><img src="'.$latest_array['display_src'].'"></a></br>';
//echo 'Likes: '.$latest_array['likes']['count'].' - Caption: '.$latest_array['caption'].'<br/>';
//echo "<script>console.log(".$results_array.");</script>";

/* BAH! An Instagram site redesign in June 2015 broke quick retrieval of captions, locations and some other stuff.
echo 'Taken at '.$latest_array['location']['name'].'<br/>';

//Heck, lets compare it to a useful API, just for kicks.
echo '<img src="http://maps.googleapis.com/maps/api/staticmap?markers=color:red%7Clabel:X%7C'.$latest_array['location']['latitude'].','.$latest_array['location']['longitude'].'&zoom=13&size=300x150&sensor=false">';
*/
?>

