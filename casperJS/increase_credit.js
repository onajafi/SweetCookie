var casper = require('casper').create();
var fs = require('fs');

casper.echo('The input file:');
casper.echo(casper.cli.args[0]);

//reading the input file:
var file_input = fs.read('../tmp/'+casper.cli.args[0]);
var parsed_input_JSON = JSON.parse(file_input);
//----------------------

var output_for_JSON = {};

casper.start('http://dining.sharif.edu/admin/payment/payment/charge');

function extract_json_file(){
    var output_filename = 'output_INC_'+parsed_input_JSON.chat_id + '.json';//GFC Get Forgotten Code
    fs.write('../tmp/'+output_filename, JSON.stringify(output_for_JSON), 'w');
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
    // Logging in
    this.sendKeys('input#loginform-username', parsed_input_JSON["user"]);
    this.sendKeys('input#loginform-password', parsed_input_JSON["pass"]);
    this.echo('STEP 1: Logging in...');
})
.thenClick('[class="btn btn-default btn-block"]')
.thenOpen("http://dining.sharif.edu/admin/payment/payment/charge")
.then(function(){
    if(this.exists('#amount-combo')) {
        // this.echo(this.getHTML('select#foodforgottencodesform-self_id'));
        output_for_JSON["PASSWORD_STATE"] = "CORRECT";
    }else{
        output_for_JSON["PASSWORD_STATE"] = "WRONG";
        extract_json_file();
        this.echo("wrong password or username");
        this.capture('navigation.png');
        this.exit();
    }
})
.then(function(){
    // this.echo(this.getHTML('#amount-combo'));
    this.evaluate(function() {
        var form = document.querySelector('#amount-combo');
        form.selectedIndex = 0;
        $(form).val(0).change();
    });
})
.then(function(){
    this.sendKeys('#paymentsform-amount', parsed_input_JSON["amount"]);
})
.thenClick('div.form-group:nth-child(6) > div:nth-child(1) > button:nth-child(2)')
.then(function(){
    this.echo('STEP 2: Waiting for the payment page to load');
    this.waitForSelector('#btnSubmit_Mellat',function(){this.echo('FOUND')},function(){this.echo('NOT_FOUND')},10000);
})
.then(function() {
    this.echo('STEP 3: Fetching the URL');

    output_for_JSON["URL"] = this.getCurrentUrl();
})
.then(function(){
    this.capture('navigation.png');

    extract_json_file();
});

casper.run();
