
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

casper.start('http://dining.sharif.edu/login');



function extract_json_file(){
    var output_filename = 'output_GFC_'+parsed_input_JSON.chat_id + '.json';//GFC Get Forgotten Code
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
    this.echo(parsed_input_JSON["pass"])
    this.echo(parsed_input_JSON["user"])
    this.echo(this.sendKeys('input#loginform-username', parsed_input_JSON["user"]));
    this.echo(this.sendKeys('input#loginform-password', parsed_input_JSON["pass"]));
    this.echo(this.getHTML('[class="btn btn-default btn-block"]'));
  }).thenClick('[class="btn btn-default btn-block"]')
  .thenOpen("http://dining.sharif.edu/admin/food/forgotten-code/forgotten-code")
  .then(function(){
    // scrape something else
    this.echo(this.getTitle());
  })
  .thenOpen("http://dining.sharif.edu/admin/food/forgotten-code/forgotten-code")
  .then(function(){
    if(this.exists('div.forgotten-code-update > div.page-title')) {
        // this.echo(this.getHTML('select#foodforgottencodesform-self_id'));
        output_for_JSON["PASSWORD_STATE"] = "CORRECT";
    }else{
        output_for_JSON["PASSWORD_STATE"] = "WRONG";
        extract_json_file();
        this.echo("wrong password or username")
    this.capture('navigation.png');
        this.exit();
    }
  })
  .then(function(){
    this.wait(3000, function(){this.echo('Waiting finished')});
  })
  .then(function(){
    this.echo("------------------------------------------------");

    this.echo(this.getHTML('select#foodforgottencodesform-self_id'));
    this.evaluate(function() {
        var form = document.querySelector('select#foodforgottencodesform-self_id');
        form.selectedIndex = 19;
        $(form).val(19).change();
    });
  })
  .then(function(){
    if(parsed_input_JSON["meal_type"] == "dinner") {
        this.echo("PPPPPPP");
        this.echo(this.getHTML('select#foodforgottencodesform-food_meal_id'));
        this.evaluate(function () {
            var form = document.querySelector('select#foodforgottencodesform-food_meal_id');
            form.selectedIndex = 2;
            $(form).val(2).change();
        });
    }
  })
  .then(function(){
      for(var i=0;i<10;i++) {//wait for 10 secs in total
          this.wait(1000, function () {});
          if(this.exists('button#get_forgotten_code_button')){
              break;
          }
      }
      this.echo('Waiting finished')
  })
  .thenClick('button#get_forgotten_code_button')
  .then(function(){
      for(var i=0;i<10;i++) {//wait for 10 secs in total
          this.wait(1000, function () {});
          if(this.exists('div.alert.alert-info.no-bottom-margin')){
              this.echo("found it!")
              break;
          }
      }
      this.echo('Waiting finished')
  })
  .then(function() {
      this.echo('-------------------------------------------');
      var forgotten_code = this.getElementInfo('div.alert.alert-info.no-bottom-margin > div').text;
      this.echo(forgotten_code);
      output_for_JSON["FCode"] = forgotten_code;
  })
  .then(function(){
    this.capture('navigation.png');

    extract_json_file();

  });

casper.run();
