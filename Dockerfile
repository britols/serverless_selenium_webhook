FROM public.ecr.aws/lambda/python@sha256:bf65727dd64fa8cbe9ada6a6c29a3fa4f248c635599e770366f8ac21eef36630 as build
RUN dnf install -y unzip && \
    curl -Lo "/tmp/chromedriver-linux64.zip" "https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.122/linux64/chromedriver-linux64.zip" && \
    curl -Lo "/tmp/chrome-linux64.zip" "https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.122/linux64/chrome-linux64.zip" && \
    unzip /tmp/chromedriver-linux64.zip -d /opt/ && \
    unzip /tmp/chrome-linux64.zip -d /opt/

FROM public.ecr.aws/lambda/python@sha256:bf65727dd64fa8cbe9ada6a6c29a3fa4f248c635599e770366f8ac21eef36630
RUN dnf install -y atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel nss mesa-libgbm

RUN pip install selenium==4.19.0
RUN pip install webdriver-manager==4.0.1
RUN pip install numpy==1.26.4
RUN pip install pandas==2.2.2
RUN pip install requests==2.30.0
RUN pip install datetime
RUN pip install lxml

COPY --from=build /opt/chrome-linux64 /opt/chrome
COPY --from=build /opt/chromedriver-linux64 /opt/
COPY main.py ./
CMD [ "main.handler" ]
