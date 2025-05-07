require 'rspec'
require 'lambda_function'

RSpec.describe Handler do
    describe "#add" do
        it "adds two numbers together" do
            handler = Handler.new
            expect(handler.add(1,2)).to eq(3) 
        end
    end
end
