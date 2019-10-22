
var casper = require('casper').create();
var x = require('casper').selectXPath;
var fs = require('fs');

casper.echo('The inputs:');
casper.echo(casper.cli.args[0]);

//reading the input file:
var file_input = fs.read('../tmp/'+casper.cli.args[0]);
var parsed_input_JSON = JSON.parse(file_input)
// require('utils').dump(parsed_JSON.pass);
//----------------------

var output_for_JSON = {};



function extract_json_file(){
    var output_filename = 'output_PLC_'+parsed_input_JSON.chat_id + '.json';
    fs.write('../tmp/'+output_filename, JSON.stringify(output_for_JSON), 'w');
}

casper.start('http://dining.sharif.edu/login');

casper.then(function() {
    var title = this.getTitle();
    this.echo('First Page: ' + title);
    if(title.search(/سامانه تغذیه/) != -1){
        output_for_JSON["ENTRY_STATE"] = "GOOD";
    }
    else{
        this.echo("Didn't load page");
        output_for_JSON["ENTRY_STATE"] = "BAD";
        extract_json_file();
        this.exit();
    }
})
.then(function(){
    this.echo(parsed_input_JSON["pass"]);
    this.echo(parsed_input_JSON["user"]);
    this.echo(this.sendKeys('input#student_student_identifier', parsed_input_JSON["user"]));
    this.echo(this.sendKeys('input#student_password', parsed_input_JSON["pass"]));
    this.echo(this.getHTML('[class="btn btn-default btn-block"]'));
}).thenClick('[class="btn btn-default btn-block"]')
.thenOpen("http://dining.sharif.edu/admin/")
.then(function(){
    // scrape something else
    this.echo(this.getTitle());
})
.thenOpen("http://dining.sharif.edu/admin/food/food-reserve/reserve")
.then(function(){
    // scrape something else
    this.echo(this.getTitle());
    if(this.exists('.navigation-link:nth-child(1)')) {
        this.echo(this.getHTML('.navigation-link:nth-child(1)'));
        output_for_JSON["PASSWORD_STATE"] = "CORRECT";
    }else{
        output_for_JSON["PASSWORD_STATE"] = "WRONG";
        extract_json_file();
        this.exit();
    }
})
/*.thenClick('.navigation-link:nth-child(1)')*/
.then(function(){
    for(var i=0;i<10;i++) {//wait for 10 secs in total
        this.wait(1000, function () {});
        if(this.exists('.navigation-link:nth-child(1)')){
            break;
        }
    }
    this.echo('Waiting finished')
})
.thenClick('.navigation-link:nth-child(1)')
.then(function(){
    this.wait(3000, function(){this.echo('Waiting finished')});
})
.then(function(){

    tempPlaceList = {};
    ref = this;
    arr_val = this.getElementsAttribute('select#foodreservesdefineform-self_id.form-control > option[value]','value');
    // require('utils').dump(arr_val);
    arr_val.forEach(function (elem_Value) {
        tmp_val = ref.getElementInfo('select#foodreservesdefineform-self_id.form-control > option[value = "' + elem_Value + '"]').text;
        tempPlaceList[elem_Value] = tmp_val;
        // require('utils').dump(tmp_val);
    });

    output_for_JSON["Place"] = tempPlaceList
})
.then(function(){
    this.echo("_________________________________________________");
    this.capture('navigation.png');
    extract_json_file();
});

casper.run();
