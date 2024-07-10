class NullWriteError(Exception): #Custom error for used by the GaussianTranslator class which is thrown if data is somehow misread or an invalid (error termination) trajectory is used.

        def __init__(self, message = "Less data than expected to write to file. Check that file exists and run did not terminate in error."):
                    
                self.message = message
                super().__init__(self.message)