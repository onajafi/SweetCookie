
var casper = require('casper').create();
var x = require('casper').selectXPath;
var fs = require('fs');

casper.echo('The inputs:');
casper.echo(casper.cli.args[0]);

//reading the input file:
var file_input = fs.read('tmp/'+casper.cli.args[0]);//extract_data_input.json
var parsed_input_JSON = JSON.parse(file_input)
// require('utils').dump(parsed_JSON.pass);
//----------------------

// var sample_text = "                   شنبه ";
var week_regex = /یک شنبه|دوشنبه|سه شنبه|چهارشنبه|پنج شنبه|جمعه|شنبه/
var date_regex = /[0-9]{4}[/][0-9]{1,2}[/][0-9]{1,2}/
var name_regex = /[\u0600-\u06FF ]*/
// casper.echo("+++++++++");
// require('utils').dump(sample_text.match(week_regex));
// casper.echo("+++++++++");
var output_for_JSON = {};

casper.start('http://dining.sharif.edu/login');

function give_meals_data_in_row(ref,row_num){
    lunch_block_selector = 'table.table.sharif-table.table-bordered.table-condensed > tbody > tr:nth-child('+ row_num +') > td.text-right'
    date_selector = 'table.table.sharif-table.table-bordered.table-condensed > tbody > tr:nth-child('+ row_num +') > th'
    temp_output = {};
    if(ref.exists(date_selector)){
        // ref.echo(ref.getElementInfo(date_selector).text);
        ref.echo(ref.getElementInfo(date_selector).text.match(week_regex));
        ref.echo(ref.getElementInfo(date_selector).text.match(date_regex));
        temp_output["day"] = ref.getElementInfo(date_selector).text.match(week_regex)[0];
        temp_output["date"] = ref.getElementInfo(date_selector).text.match(date_regex)[0];
    }
    else{
        temp_output["day"] = "";
        temp_output["date"] = "";
    }

    temp_output["meal_arr"] = [];
    if(ref.exists(lunch_block_selector)) {
        ref.echo(ref.getElementInfo(lunch_block_selector).text);
        for(var i=1;;i++) {
            meal_selector = lunch_block_selector + '> div.food-reserve-diet-div.has-mini-bottom-padding:nth-child(' + i + ')';
            if (ref.exists(meal_selector)) {
                var temp_meal = {};
                meal_dat = ref.getElementInfo(meal_selector);
                ref.echo("++++" + i);
                ref.echo(meal_dat.text);
                temp_meal["meal_name"] = meal_dat.text;

                //Check if it has been reserved:
                if(ref.exists(meal_selector + '> span.fa.fa-check.fa-lg.has-left-margin.has_tooltip')){
                    ref.echo('CONFIRMED!');
                    temp_meal["status"] = "OK_DONE";
                }
                else if(ref.exists(meal_selector + '> span.fa.fa-shopping-cart.fa-lg.has-left-margin.cursor_pointer.has_tooltip')){
                    ref.echo("You can still get it...");
                    temp_meal["status"] = "AWAITING";
                }
                else if(ref.exists(meal_selector + '> span.fa.fa-times-circle.fa-lg.has-left-margin.cursor_pointer.has_tooltip')){
                    ref.echo('Confirmed - But may get canceled...');
                    temp_meal["status"] = "OK_AWAITING";
                }
                else{
                    ref.echo("Nope you lost it!!!");
                    temp_meal["status"] = "FAILED";
                }
                temp_output["meal_arr"].push(temp_meal);
            }else {
                break;
            }
        }
    }else{
        // ref.echo("INCORRECT ROW NUMBER: " + row_num);
        ref.echo("EMPTY ROW: " + row_num)
    }
    return temp_output;
}

function give_meal_data_in_table(ref){
    var table_output=[];
    for(var j=1;j<=7;j++){
        ref.echo('================');
        table_output.push(give_meals_data_in_row(ref,j));
    }
    return table_output
}

//Get stuff like the users name, and account credit balance
function get_balance_info(ref){
    credit_balance_selector = 'span.main_balance_span.balance_negative';
    if(ref.exists(credit_balance_selector)) {
        ref.echo(parseFloat(ref.getElementInfo(credit_balance_selector).text.replace(",", ".")));
        return parseFloat(ref.getElementInfo(credit_balance_selector).text.replace(",", "."));
    }
    else{//Looks like the balance is positive $_$
        credit_balance_selector = 'span.main_balance_span';
        if(ref.exists(credit_balance_selector)) {
            ref.echo(parseFloat(ref.getElementInfo(credit_balance_selector).text.replace(",", ".")));
            return parseFloat(ref.getElementInfo(credit_balance_selector).text.replace(",", "."));
        }
    }
    return -1;
}

function extract_json_file(){
    var output_filename = 'output_EXT_'+parsed_input_JSON.chat_id + '.json';
    fs.write('tmp/'+output_filename, JSON.stringify(output_for_JSON), 'w');
}

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
    this.echo(parsed_input_JSON["pass"])
    this.echo(parsed_input_JSON["user"])
    this.echo(this.sendKeys('input#loginform-username', parsed_input_JSON["user"]));
    this.echo(this.sendKeys('input#loginform-password', parsed_input_JSON["pass"]));
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
    .then(function(){
    this.wait(4000, function(){this.echo('Waiting finished')});
    })
    .then(function(){
        // this.echo("------------------------------------------------");

        // this.echo(parsed_input_JSON["PLCnum"]);
        // this.echo(Number(parsed_input_JSON["PLCnum"]));
        // this.echo(this.getHTML('select#foodreservesdefineform-self_id'));

        this.evaluate(function(row_value) {
            var form = document.querySelector('select#foodreservesdefineform-self_id');
            form.selectedIndex = row_value;
            $(form).val(row_value).change(); //TODO do something about the values (#19 is just for the boys section)

        },parsed_input_JSON["PLCnum"]);


    })
    .then(function(){
    this.wait(3000, function(){this.echo('Waiting finished')});
    })
  .then(function(){
    output_for_JSON["Table"] = give_meal_data_in_table(this);
    this.echo("------------------------------------------------");
    output_for_JSON["Balance"] = get_balance_info(this);

    this.capture('navigation.png');

    extract_json_file();

  });

casper.run();
