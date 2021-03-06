from distutils.core import setup
setup(
  name = 'zammad_api',         # How you named your package folder (MyLib)
  packages = ['zammad_api'],   # Chose the same as "name"
  version = '0.1.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Work with the Zammad API',   # Give a short description about your library
  author = 'Twilight Sparkle',                   # Type in your name
  author_email = 'spam@twilightsparkle.dev',      # Type in your E-Mail
  url = 'https://github.com/Twi1ightSparkle/zammad_api',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Twi1ightSparkle/zammad_api/archive/v0.1.4.tar.gz',    # I explain this later on
  keywords = ['zammad', 'api'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.8',
  ],
)