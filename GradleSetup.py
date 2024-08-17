import os
import shutil
import subprocess

class GradleSetup():
    def __init__(self, directory):
        self.directory = directory

        if self._check_gradle():
            print(f"[INFO] Gradle project initialized.")
        else:
            print(f"[INFO] Gradle project not initialized.")
            self._init_gradle()
        
        self.src = os.path.join(self.directory, 'app', 'src')

        self._init_jacoco()

        self.test()
    
    def _check_gradle(self) -> bool:
        gradle_files = ["gradlew", "settings.gradle"]

        for file in os.listdir(self.directory):
            if file in gradle_files:
                return True
        return False
    
    def _init_gradle(self):
        print('[INFO] Staring gradle')
        try:
            process = subprocess.Popen(
                ['gradle', 'init', '--type', 'java-application', '-p', self.directory, '--dsl', 'groovy'],
                stdin=None,  
                stdout=None,  
                stderr=None
            )
            
            process.communicate()
            
            if process.returncode == 0:
                print(f"[INFO] Gradle project initialized successfully at {self.directory}.")
            else:
                print(f"Gradle init failed with return code {process.returncode}.")
    
        except Exception as e:
            print(f"An error occurred: {e}")
        
        if os.path.exists(os.path.join(self.directory, 'src')):
            shutil.rmtree(os.path.join(self.directory, 'app', 'src'))
        
            shutil.copytree(os.path.join(self.directory, 'src'), os.path.join(self.directory, 'app', 'src'))
            shutil.rmtree(os.path.join(self.directory, 'src'))
    
    def _init_jacoco(self):
        """Add JaCoCo test coverage plugin and configuration to the Gradle build file."""
        build_gradle_path = os.path.join(self.directory, 'app', 'build.gradle')

        # JaCoCo plugin and configuration
        jacoco_config = """
jacoco {
    toolVersion = "0.8.11"
}

test {
    useJUnitPlatform() 
    finalizedBy jacocoTestReport 
}

jacocoTestReport {
    reports {
        xml.required =  true
        html.required = true
    }
}
        """
        if os.path.exists(build_gradle_path):
            with open(build_gradle_path, 'r') as file:
                content = file.read()

            # Append JaCoCo plugin if not already added
            if "id 'jacoco'" not in content:
                content = content.replace("plugins {", "plugins {\n    id 'jacoco'")

            # Append JaCoCo configuration if not already added
            if "jacoco {" not in content:
                content += jacoco_config

            # Write the updated content back to build.gradle
            with open(build_gradle_path, 'w') as file:
                file.write(content)

            print(f"[INFO] JaCoCo configuration added to {build_gradle_path}")
        else:
            raise Exception(f"build.gradle file not found.")
    
    def test(self):
        try:
            result = subprocess.run(
                ['gradle', 'test', 'jacocoTestReport', '-p', self.directory],
                check=True,  
                capture_output=True,  
                text=True  
            )
            print(result.stdout)
    
        except subprocess.CalledProcessError as e:
            print(e.stderr)
            print(e.stdout)
            print(f"Gradle command failed with error code {e.returncode}")
            raise  

if __name__=='__main__':

    g = GradleSetup('root')
    g.test()