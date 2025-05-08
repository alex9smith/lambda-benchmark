require 'rspec'
require 'lambda_function'

RSpec.describe Lambda do
    describe "#add" do
        it "adds two numbers together" do
            handler = 
            expect(Lambda::Handler.add(1,2)).to eq(3) 
        end
    end
end
