# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 The Regents of the University of California
#
# This file is part of BRAILS.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# You should have received a copy of the BSD 3-Clause License along with
# BRAILS. If not, see <http://www.opensource.org/licenses/>.
#
# Contributors:
# Barbaros Cetiner

#
# NOTE: Originally this was the RoofClassifier class in brails--
#

from brails.processors.image_classifier.image_classifier import ImageClassifier
from brails.types.image_set import ImageSet
from typing import Optional, Dict

import torch
import os

class RoofShapeClassifier(ImageClassifier):

    """
    The RoofShape classifier attempts to predict roof shapes into 1 of 3 types: Flat, Hip, or Gable. The classification is done
    by the ImageClassifier class. This class is a wrapper that just sets up the inputs for that class.

    Variables
       model_path: str Path to the model file
    
    Methods:
       predict(ImageSet): To return the predictions for the set of images provided

    """
    
    def __init__(self, input_data: Optional[dict] =None): 

        """
        The class constructor sets up the path to the trained model file. If no model is provided, the class downloads a default
        from the web for this and subseqyet use.
        
        Args
            input_data: dict Optional. The init function looks for a 'model_path' key to set model_path.
        """

        #
        # if input_data, check if it contains 'modelPath' key and also pass on to base class
        #
        
        if not input_data == None:
            super().__init__(input_data)
            model_path = input_data['modelPath']
        else:
            model_path = None

        #
        # if no model_file provided, use one previosuly downloaded or got get if if not existing
        #
        
        if model_path == None:
            os.makedirs('tmp/models',exist_ok=True)
            model_path = 'tmp/models/roofTypeClassifier_v1.pth'
            if not os.path.isfile(model_path):
                print('\n\nLoading default roof classifier model file to tmp/models folder...')
                torch.hub.download_url_to_file('https://zenodo.org/record/7271554/files/trained_model_rooftype.pth',
                                               model_path, progress=True)
                print('Default roof classifier model loaded')
            else: 
                print(f"\nDefault roof classifier model at {model_path} loaded")
        else:
            print(f'\nInferences will be performed using the custom model at {model_path}')
        
        self.model_path = model_path
        self.classes = ['Flat','Gable','Hip']      
        
    def predict(self, images: ImageSet) ->dict:

        """
        The method predicts the roof shape.
        
        Args
            images: ImageSet The set of images for which a prediction is required

        Returns
            dict: The keys being the same keys used in ImageSet.images, the values being the predicted roof shape
        """
        
        imageClassifier = ImageClassifier()
        return imageClassifier.predict(images, self.model_path, self.classes)
        
    def retrain(self, dataDir, batchSize=8, nepochs=100, plotLoss=True):
        imageClassifier = ImageClassifier()
        imageClassifier.retrain(self.model_path, dataDir, batchSize, nepochs, plotLoss)
        
if __name__ == '__main__':
    pass        
