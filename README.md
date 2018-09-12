# fantasypoints

This library attempts to provide an easy way to display stats of NFL players and teams for fantasy football in your web browser.

Fantasypoints heavily relies on the [nfldb](https://github.com/BurntSushi/nfldb) project. Due to this, this project only works with python 2.7 and requires a postgres database.

## Setup

This project requires nfldb, installing it is described in the [nfldb wiki](https://github.com/BurntSushi/nfldb#installation-and-dependencies).

After setting up nfldb, generate a json file for the web server to run.

```shell
python2 build-json.py 2017
```

This will run the query at `2017.sql` on the nfldb database and genertae a json file at `2017.json`.

Once you have a json file, edit the ajax source in `main.js`.

```javascript
var table = $('#scores').DataTable({
  ajax: {
    url: '2017.json',
    dataSrc: ''
  },

...
```

## Running

If you want to get up and running locally, just open `index.html` in your web browser.

If you want to serve as a web application, use your favorite static web server (ex. [nginx](https://nginx.org/) or [apache](https://httpd.apache.org/)) to host the webfiles and json file.

## Customization

Changing the data generated requires editing `build-json.py` and/or creating a custom sql query. It may also require altering the web files. The main table is created using [DataTables](https://www.datatables.net/) and can be altered using the DataTables API.

Changing the styles of the table can be done by changing `main.css`.
