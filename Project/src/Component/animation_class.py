from imageLoader_class import ImageLoader

class Animation:
    def __init__(self,imgsrc, size=1.0, loop=False,animFrame=24):
        self.mImageArray=[]
        self.mCurrentFrame=0
        self.mAnimFrame=24
        self.mSize=size
        self.mLoop=loop
        imgloader=ImageLoader()

        for src in imgsrc:
            self.mImageArray.append(imgloader.load_image(src))
        self.mSelectImage=self.mImageArray[0]
    
    def Update(self, deltaTime):
        if self.mLoop:
            self.mCurrentFrame+= self.mAnimFrame*deltaTime
            while self.mCurrentFrame>len(self.mImageArray)-1:
                self.mCurrentFrame-=len(self.mImageArray)
            self.mSelectImage=self.mImageArray[int(self.mCurrentFrame)]
        else:
            self.mCurrentFrame+= self.mAnimFrame*deltaTime
            if self.mCurrentFrame>len(self.mImageArray)-1:
                self.mSelectImage=self.mImageArray[len(self.mImageArray)-1]
            else:
                self.mSelectImage=self.mImageArray[int(self.mCurrentFrame)]
        
                
        
def ExplosionAnim():
    imgsrc=[]
    for i in range(1, 42):
        imgsrc.append('Project\\assets\\explosion\\'+str(i)+'.png')
    return Animation(imgsrc,0.1)